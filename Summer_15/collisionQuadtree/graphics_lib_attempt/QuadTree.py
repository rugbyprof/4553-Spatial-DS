import sys
sys.path.append("../ShapeModules")
from Point import Point
from BoundingBox import BoundingBox
from Polygon import Polygon
import pantograph

class QuadTree(object):

    def __init__(self,bbox,maxPoints):
        self.northEast = None
        self.southEast = None
        self.southWest = None
        self.northWest = None

        self.points = []
        self.bbox = bbox
        self.maxPoints = maxPoints
        self.smallestContainer = None

    def __str__(self):
        return "\nnorthwest: %s,\nnorthEast: %s,\nsouthWest: %s,\nsouthEast: %s,\npoints: %s,\nbbox: %s,\nmaxPoints: %s\n" % (self.northWest, self.northEast,self.southWest, self.southEast,self.points,self.bbox,self.maxPoints)

    """
    Insert a new point into this QuadTree node
    """
    def insert(self,point):
        if not self.bbox.containsPoint(point):
            return False

        if len(self.points) < self.maxPoints:
            # If we still have spaces in the bucket array for this QuadTree node,
            #    then the point simply goes here and we're finished
            self.points.append(point)
            return True
        elif self.northEast == None:
            # Otherwise we split this node into NW/NE/SE/SW quadrants
            self.subdivide()

        # Insert the point into the appropriate quadrant, and finish
        if ((self.northEast.insert(point)) or (self.southEast.insert(point)) or
            (self.southWest.insert(point)) or (self.northWest.insert(point))):
            return True

        # If we couldn't insert the new point, then we have an exception situation
        raise ValueError('Point is outside bounding box!')

    """
     Split this QuadTree node into four quadrants for NW/NE/SE/SW
    """
    def subdivide(self):
        #print "self:",self.bbox
        l = self.bbox.ul.x
        r = self.bbox.lr.x
        t = self.bbox.ul.y
        b = self.bbox.lr.y
        mX = (l+r) / 2
        mY = (t+b) / 2
        self.northEast = QuadTree(BoundingBox(Point(mX,t),Point(r,mY)),self.maxPoints)
        self.southEast = QuadTree(BoundingBox(Point(mX,mY),Point(r,b)),self.maxPoints)
        self.southWest = QuadTree(BoundingBox(Point(l,mY),Point(mX,b)),self.maxPoints)
        self.northWest = QuadTree(BoundingBox(Point(l,t),Point(mX,mY)),self.maxPoints)
        #print self.northEast,self.southEast,self.southWest,self.northWest


    """
     Return an array of all points within this QuadTree and its child nodes that fall
     within the specified bounding box
    """
    def searchBox(self,bbox):

        results = []

        if self.bbox.overlaps(bbox) or self.bbox.containsBox(bbox):
            # Test each point that falls within the current QuadTree node
            for p in self.points:
                # Test each point stored in this QuadTree node in turn, adding to the results array
                #    if it falls within the bounding box
                if self.bbox.containsPoint(p):
                    results.append(p)


            # If we have child QuadTree nodes....
            if (not self.northWest == None):
                # ... search each child node in turn, merging with any existing results
                results = results + self.northWest.searchBox(self.bbox)
                results = results + self.northEast.searchBox(self.bbox)
                results = results + self.southWest.searchBox(self.bbox)
                results = results + self.southEast.searchBox(self.bbox)

        return results

    """
     Returns the containers points that are in the same container as another point.
    """
    def searchNeighbors(self,point):

        #If its not a point (its a bounding rectangle)
        if not hasattr(point, 'x'):
            return []

        results = []

        if self.bbox.containsPoint(point):
            print point," in ",self.bbox
            # Test each point that falls within the current QuadTree node
            for p in self.points:
                print p
                # Test each point stored in this QuadTree node in turn, adding to the results array
                #    if it falls within the bounding box
                if self.bbox.containsPoint(p):
                    print p," in bbox"
                    results.append(p)


            # If we have child QuadTree nodes....
            if (not self.northWest == None):
                # ... search each child node in turn, merging with any existing results
                results = results + self.northWest.searchNeighbors(point)
                results = results + self.northEast.searchNeighbors(point)
                results = results + self.southWest.searchNeighbors(point)
                results = results + self.southEast.searchNeighbors(point)

        return results

    def getSmallestBBox(self,point):

        if self.bbox.containsPoint(point):
            print "smallest..."
            print self.bbox

            if (not self.northWest == None):
                print "checking others"
                self.northWest.getSmallestBBox(point)
                self.northEast.getSmallestBBox(point)
                self.southWest.getSmallestBBox(point)
                self.southEast.getSmallestBBox(point)

            self.smallestContainer = self.bbox
    """
    Print helper to draw tree
    """
    def getBBoxes(self):
        bboxes = []

        bboxes.append(self.bbox)

        if (not self.northWest == None):
            # ... search each child node in turn, merging with any existing results
            bboxes = bboxes + self.northWest.getBBoxes()
            bboxes = bboxes + self.northEast.getBBoxes()
            bboxes = bboxes + self.southWest.getBBoxes()
            bboxes = bboxes + self.southEast.getBBoxes()

        return bboxes

if __name__ == '__main__':

    class Driver(pantograph.PantographHandler):

        def setup(self):
            self.q = QuadTree(BoundingBox(Point(0,0),Point(self.width,self.height)),3)
            self.points = []
            self.colors = ["#000","#F00","#0f0","#00f","#ff0","#0ff","#0f0"]

        def on_mouse_down(self,InputEvent):
            #print InputEvent
            if InputEvent.shift_key == True:
                self.q.getSmallestBBox(Point(InputEvent.x,InputEvent.y))
                print self.q.smallestContainer

            self.q.insert(Point(InputEvent.x,InputEvent.y))
            self.points.append(Point(InputEvent.x,InputEvent.y))
            self.bboxs = self.q.getBBoxes()
            print "click: ",InputEvent.x,InputEvent.y


        def drawShapes(self):
            self.draw_rect(0, 0, self.width, self.height, color= "#000")
            self.fill_oval(self.width/2, self.height/2, 7, 7, "#F00")

            for p in self.points:
                self.fill_oval(p.x, p.y, 7, 7, "#F00")

            self.bboxs = self.q.getBBoxes()
            for b in self.bboxs:
                self.draw_rect(b.ul.x,b.ul.y,b.w,b.h,"#000")

        def update(self):
            self.clear_rect(0, 0, self.width, self.height)
            self.drawShapes()


    app = pantograph.SimplePantographApplication(Driver)
    app.run()
