import math
import random
import numpy as np
import time
from pointQuadTree import *
# Add ShapeModules (which holds Point,Rect,Polygon) folder to the path
# so we can use those shapes.
import sys
sys.path.append("../ShapeModules")
from BoundingBox import *
import pantograph


class RectQuadTree(object):

    def __init__(self,bbox,maxPoints):
        self.northEast = None
        self.southEast = None
        self.southWest = None
        self.northWest = None

        self.rects = []
        self.bbox = bbox
        self.maxPoints = maxPoints

    def __str__(self):
        return "\nnorthwest: %s,\nnorthEast: %s,\nsouthWest: %s,\nsouthEast: %s,\npoints: %s,\nbbox: %s,\nmaxPoints: %s\n" % (self.northWest, self.northEast,self.southWest, self.southEast,self.points,self.bbox,self.maxPoints)

    """
    Insert a new point into this QuadTree node
    """
    def insert(self,r):
        if not self.bbox.overlaps(r):
            #print "Point %s is not inside bounding box %s" % (point,self.bbox)
            return False

        if len(self.rects) < self.maxPoints:
            # If we still have spaces in the bucket array for this QuadTree node,
            #    then the point simply goes here and we're finished
            self.rects.append(r)
            return True
        elif self.northEast == None:
            print("subdividing")
            # Otherwise we split this node into NW/NE/SE/SW quadrants
            self.subdivide()

        # Insert the point into the appropriate quadrant, and finish
        if ((self.northEast.insert(r)) or (self.southEast.insert(r)) or
            (self.southWest.insert(r)) or (self.northWest.insert(r))):
            return True

        # If we couldn't insert the new point, then we have an exception situation
        raise ValueError("Rect %s is outside bounding box %s" % (r,self.bbox))

    """
     Split this QuadTree node into four quadrants for NW/NE/SE/SW
    """
    def subdivide(self):
        l = self.bbox.ul.x
        r = self.bbox.lr.x
        t = self.bbox.ul.y
        b = self.bbox.lr.y
        mX = (l+r) / 2
        mY = (t+b) / 2
        self.northEast = RectQuadTree(BoundingBox(Point(mX,t),Point(r,mY)),self.maxPoints)
        self.southEast = RectQuadTree(BoundingBox(Point(mX,mY),Point(r,b)),self.maxPoints)
        self.southWest = RectQuadTree(BoundingBox(Point(l,mY),Point(mX,b)),self.maxPoints)
        self.northWest = RectQuadTree(BoundingBox(Point(l,t),Point(mX,mY)),self.maxPoints)


    """
     Return an array of all items within this QuadTree and its child nodes that fall
     within the specified bounding box
    """
    def searchBox(self,bbox):

        results = []

        if self.bbox.overlaps(bbox) or self.bbox.containsBox(bbox):
            # Test each point that falls within the current QuadTree node
            for r in self.rects:
                # Test each point stored in this QuadTree node in turn, adding to the results array
                #    if it falls within the bounding box
                if self.bbox.containsBox(r):
                    results.append(r)


            # If we have child QuadTree nodes....
            if (not self.northWest == None):
                # ... search each child node in turn, merging with any existing results
                results = results + self.northWest.searchBox(self.bbox)
                results = results + self.northEast.searchBox(self.bbox)
                results = results + self.southWest.searchBox(self.bbox)
                results = results + self.southEast.searchBox(self.bbox)

        return results

    """
     Returns the containers items that are in the same container as another point.
    """
    def searchNeighbors(self,bbox):


        results = []

        if self.bbox.containsBox(bbox):
            # Test each point that falls within the current QuadTree node
            for r in self.bbox:
                # Test each point stored in this QuadTree node in turn, adding to the results array
                #    if it falls within the bounding box
                if self.bbox.containsBox(r):
                    results.append(r)


            # If we have child QuadTree nodes....
            if (not self.northWest == None):
                # ... search each child node in turn, merging with any existing results
                results = results + self.northWest.searchNeighbors(bbox)
                results = results + self.northEast.searchNeighbors(bbox)
                results = results + self.southWest.searchNeighbors(bbox)
                results = results + self.southEast.searchNeighbors(bbox)

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
A vector can be determined from a single point when basing
it from the origin (0,0), but I'm going to assume 2 points.
Example:
    AB = Vector(Point(3,4),Point(6,7))

or if you want to use the origin

    AB = Vector(Point(0,0),Point(8,4))

"""
class Vector(object):
    def __init__(self,p1,p2):
        assert not p1 == None
        assert not p2 == None
        self.p1 = p1
        self.p2 = p2
        self.v = [self.p1.x - self.p2.x, self.p1.y - self.p2.y]
        self.a,self.b = self.v

    def _str__(self):
        return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\nb: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)

    def __repr__(self):
        return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\nb: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)

class VectorOps(object):
    def __init__(self,p1=None,p2=None,velocity=1):
        self.p1 = p1
        self.p2 = p2
        self.dx = 0
        self.dy = 0
        if not self.p1 == None and not self.p2 == None:
            self.v = Vector(p1,p2)
            self.velocity = velocity
            self.magnitude = self._magnitude()
            self.bearing = self._bearing()
            self.step = self._step()
        else:
            self.v = None
            self.velocity = None
            self.bearing = None
            self.magnitude = None

    """
    Calculate the bearing (in radians) between p1 and p2
    """
    def _bearing(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        rads = math.atan2(-dy,dx)
        return rads % 2*math.pi         # In radians
        #degs = degrees(rads)
    """
    A vector by itself can have a magnitude when basing it on the origin (0,0),
    but in this context we want to calculate magnitude (length) based on another
    point (converted to a vector).
    """
    def _magnitude(self):
        assert not self.v == None
        return math.sqrt( (self.v.a**2) + (self.v.b**2) )

    """
    Create the step factor between p1 and p2 to allow a point to
    move toward p2 at some interval based on velocity. Greater velocity
    means bigger steps (less granular).
    """
    def _step(self):
        cosa = math.sin(self.bearing)
        cosb = math.cos(self.bearing)
        self.dx = cosa * self.velocity
        self.dy = cosb * self.velocity
        return [cosa * self.velocity, cosb * self.velocity]

    def _str__(self):
        return "[\n vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s\n, step: %s\n]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)

    def __repr__(self):
        return "[\n vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s\n, step: %s\n]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)



class Rock():
    def __init__(self, center, radius,velocity=1,color="#000"):
        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.x = center.x
        self.y = center.y
        self.center = center
        self.dest = self.destination(100,math.radians(random.randint(0,360)))
        self.vectorOps = VectorOps(self.center,self.dest,self.velocity)
        self.color = color

    def destination(self,distance,bearing):
        cosa = math.sin(bearing)
        cosb = math.cos(bearing)
        return Point(self.x + (distance * cosa), self.y + (distance * cosb))

    def move(self,bounds):
        x = self.x
        y = self.y
        #Move temporarily
        x += self.vectorOps.dx
        y += self.vectorOps.dy

        #Check if in bounds
        #If it's not, then change direction
        if not self.xInBounds(bounds,x):
            self.vectorOps.dx *= -1
        if not self.yInBounds(bounds,y):
            self.vectorOps.dy *= -1

        #Move any way
        self.x += self.vectorOps.dx
        self.y += self.vectorOps.dy

        self.center.x = self.x
        self.center.y = self.y


    def xInBounds(self,bounds,x):
        if x >= bounds.maxX or x <= bounds.minX :
            return False

        return True

    def yInBounds(self,bounds,y):
        if y >= bounds.maxY or y <= bounds.minY:
            return False

        return True



    def _str__(self):
        return "[\n center: %s,\n radius: %s,\n vector: %s,\n speed: %s\n ]" % (self.center,self.radius, self.vectorOps,self.velocity)

    def __repr__(self):
        return "[\n center: %s,\n radius: %s,\n vector: %s,\n speed: %s\n ]" % (self.center, self.radius, self.vectorOps,self.velocity)


class Bounds(object):
    def __init__(self,minx,miny,maxx,maxy):
        self.minX = minx
        self.minY = miny
        self.maxX = maxx
        self.maxY = maxy
    def __repr__(self):
        return "[%s %s %s %s]" % (self.minX, self.minY, self.maxX,self.maxY)


class Driver(pantograph.PantographHandler):
    def setup(self):
        self.bounds = Bounds(0,0,self.width,self.height)
        self.rockSpeeds = np.arange(1,15,1)
        self.numRocks = 50
        self.qt = PointQuadTree(BoundingBox(Point(0,0),Point(self.width,self.height)),1)
        self.rockSize = 5
        self.halfSize = self.rockSize / 2
        self.rocks = []
        self.boxes = []

        for i in range(self.numRocks):

            speed = random.choice(self.rockSpeeds)

            r = Rock(self.getRandomPosition(),self.rockSize,speed,"#F00")
            self.rocks.append(r)
            self.qt.insert(r)

    def update(self):
        self.moveRocks()
        self.clear_rect(0, 0, self.width, self.height)
        self.drawRocks()
        self.drawBoxes();
        #time.sleep(.5)

    def checkCollisions(self,r):
        box = BoundingBox(Point(r.center.x-self.halfSize,r.center.y-self.halfSize),Point(r.center.x+self.halfSize,r.center.y+self.halfSize))
        boxes  = self.qt.searchBox(box)
        boxes.sort(key=lambda tup: tup[1],reverse=True)
        #print boxes
        #print


    def getRandomPosition(self):
        x = random.randint(0+self.rockSize,int(self.width)-self.rockSize)
        y = random.randint(0+self.rockSize,int(self.height)-self.rockSize)
        return Point(x,y)

    def drawBoxes(self):
        boxes = self.qt.getBBoxes()
        for box in boxes:
            self.draw_rect(box.ul.x,box.ul.y,box.w,box.h)

    def drawRocks(self):
        for r in self.rocks:
            self.fill_circle(r.x,r.y,r.radius,r.color)

    def moveRocks(self):
        self.qt = PointQuadTree(BoundingBox(Point(0,0),Point(self.width,self.height)),1)
        for r in self.rocks:
            self.checkCollisions(r)
            r.move(self.bounds)
            self.qt.insert(r)


if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()
