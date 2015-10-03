import math
import random
import numpy as np
from QuadTree import QuadTree

# Add ShapeModules (which holds Point,Rect,Polygon) folder to the path
# so we can use those shapes.
import sys
from graphics import *

class BoundingBox(object):

    """
    Initialize a rectangle from two points.
    ul = upper LEFT
    lr = lower RIGHT
    """
    def __init__(self, ul=None, lr=None):
        if not ul:
            ul = Point()
        if not lr:
            lr = Point()

        self.set_points(ul, lr)
        self.parent = None

    """
    Reset the bbox coordinates.
    """
    def set_points(self, ul, lr):
        self.ul = ul
        self.lr = lr
        self.w = math.fabs(ul.x-lr.x)
        self.h = math.fabs(ul.y-lr.y)
        self.center = Point((math.fabs(self.ul.x-self.lr.x)/2),(math.fabs(self.ul.y-self.lr.y)/2))


    """
    Return true if a point is inside the rectangle.
    """
    def containsPoint(self, p):

        #print "ul: ",self.ul,self.ul.x,",",self.ul.y
        #print "lr: ",self.lr

        #print p.x," < ",self.ul.x," and ",p.x," < ",self.lr.x," and ",p.y," > ",self.ul.y ," and ",p.y," < ",self.lr.y

        return (p.x > self.ul.x and p.x < self.lr.x and p.y > self.ul.y and p.y < self.lr.y)

    """
    Return true if a rect is inside this rectangle.
    """
    def containsBox(self, other):
        return (self.ul.x < other.ul.x and other.ul.y > self.ul.y and other.lr.x < self.lr.x and other.lr.y < self.lr.y)


    """
    Return true if a rectangle overlaps this rectangle.
    """
    def overlaps(self, other):
        return not ((min(other.ul.x,other.lr.x) > max(self.ul.x,self.lr.x)) or
               (min(self.ul.x,self.lr.x) > max(other.ul.x,other.lr.x)))

    """
    Return a rectangle with extended borders.

    Create a new rectangle that is wider and taller than the
    immediate one. All sides are extended by "n" points.
    """
    def expanded_by(self, n):
        p1 = Point(self.left-n, self.top-n)
        p2 = Point(self.right+n, self.bottom+n)
        return Rect(p1, p2)

    def __str__( self ):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.ul.x,self.ul.y,self.lr.x,self.lr.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,Point(self.ul.x, self.ul.y),Point(self.lr.x, self.lr.y))

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


"""
Sketchy way to calculate a movement Vector that can be applied to a point (x,y)
essentially moving it in the correct direction (with respect to some end point)
at a specified velocity (aka moving at some speed toward some point)
"""
class PointVector(object):
    def __init__(self,start=None,end=None,bearing=0,velocity=1):
        self.start = start
        self.end = end
        self.velocity = velocity
        self.bearing = math.radians(bearing)

    def _str__(self):
        return "[\n start: %s,\n end: %s,\n bearing: %s,\n velocity: %s\n]" % (self.start, self.end, self.bearing,self.velocity)

    def __repr__(self):
        return "[\n start: %s,\n end: %s,\n bearing: %s,\n velocity: %s\n]" % (self.start, self.end, self.bearing,self.velocity)

    """
    Setters
    """
    def Start(self):
        self.start = start

    def End(self):
        self.end = end

    def Velocity(self,velocity):
        self.velocity = velocity

    def Bearing(self,bearing):
        bearing = float(bearing)
        self.bearing = math.radians(bearing)
        return

    def Destination(self,distance,bearing=None):
        if bearing == None:
            bearing = self.bearing
        cosa = math.sin(bearing)
        cosb = math.cos(bearing)
        self.end = Point(self.start.x + (distance * cosa), self.start.y + (distance * cosb))
        return self.end

    """
    Calculate a movement vector to be applied to a point to move it on the
    current bearing at current velocity
    """
    def Vector(self,start=None,end=None,bearing=None,velocity=None):
        if start == None:
            start = self.start
        if end == None:
            end = self.end
        if bearing == None:
            bearing = self.bearing
        if velocity == None:
            velocity = self.velocity
        # Calculate the Norm
        diff = [start.x - end.x, start.y - end.y]
        norm = math.sqrt(diff[0]**2 + diff[1]**2)
        bearing = [diff[0]/norm, diff[1]/norm]
        self.vector = [bearing[0] * velocity, bearing[1] * velocity]
        return self.vector



class Rock(Oval):
    def __init__(self, center, radius):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius
        self.move = PointVector(center)
        self.x = center.x
        self.y = center.y

    def deltaMove(self):
        vector = self.move.Vector()
        print vector
        self.x += vector[0]
        self.y += vector[1]

    def _str__(self):
        return "[\n center: %s,\n radius: %s,\n vector: %s,\n ]" % (self.p1, self.radius, self.move)

    def __repr__(self):
        return "[\n center: %s,\n radius: %s,\n vector: %s,\n ]" % (self.p1, self.radius, self.move)


class Driver(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.rockSpeeds = np.arange(1,15,1)
        self.numRocks = 15
        self.q = QuadTree(BoundingBox(Point(5,5),Point(self.width,self.height)),1)
        self.rockSize = 5
        self.win = GraphWin("Testing", self.width, self.height, autoflush=False)
        self.rocks = []
        self.boxes = []

        xWalls = [0,self.width]
        yWalls = [0,self.height]

        self.win.addItem(Rectangle(Point(5,5),Point(self.width,self.height)))
        self.win.redraw()

        for i in range(self.numRocks):
            #click = self.win.getMouse() # Pause to view result

            startX = random.randint(0+self.rockSize,int(self.width)-self.rockSize)
            startY = random.randint(0+self.rockSize,int(self.height)-self.rockSize)

            speed = random.choice(self.rockSpeeds)

            #r = Rock(Point(click.getX(),click.getY()),self.rockSize)
            r = Rock(Point(startX,startY),self.rockSize)
            r.move.Destination(random.randint(self.width/2,self.width),random.randint(0,360))
            self.rocks.append(r)
            self.q.insert(r)
            self.win.addItem(r)

        self.win.redraw()

        # self.drawBoxes()
        while True:
            self.moveRocks()
            self.win.getMouse()
            self.win.redraw()

        self.win.getMouse() # Pause to view result
        self.win.close()    # Close window when done

    def drawBoxes(self):
        boxes = self.q.getBBoxes()
        for box in boxes:
            box = Rectangle(box.ul,box.lr)
            box.draw(self.win)

    def drawRocks(self):
        for r in self.rocks:
            r.draw(self.win)


    def moveRocks(self):
        for r in self.rocks:
            print r
            r.deltaMove()
            print r

if __name__ == '__main__':
    D = Driver(500,500)
