import math
import random
import numpy as np
from QuadTree import QuadTree
import time

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

        return ( self.ul.x <= p.x and p.x <= self.lr.x and self.ul.y <= p.y and p.y <= self.lr.y )

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
            #print "Point %s is not inside bounding box %s" % (point,self.bbox)
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
        raise ValueError("Point %s is outside bounding box %s" % (point,self.bbox))

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


class Rock(Circle):
    def __init__(self,p,radius):
        p1 = Point(p.x-radius, p.y-radius)
        p2 = Point(p.x+radius, p.y+radius)
        Circle.__init__(self, p, radius)
        self.x = p.x
        self.y = p.y
        self.radius = radius
        self.bearing = math.radians(random.randint(0,360))
        self.velocity = random.randint(1,10)
        self.vectorOps = VectorOps(p,self.destination(100,self.bearing),self.velocity)

    def destination(self,distance,bearing):
        cosa = math.sin(bearing)
        cosb = math.cos(bearing)
        return Point(self.x + (distance * cosa), self.y + (distance * cosb))

    def dx(self):
        return self.vectorOps.dx

    def dy(self):
        return self.vectorOps.dy

    def __str__(self):
        return "[\n x: %s,\n y: %s,\n radius: %s,\n vector: %s\n]" % (self.x, self.y, self.radius,self.vectorOps)


class Driver(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.rockSpeeds = np.arange(1,15,1)
        self.numRocks = 25
        self.q = QuadTree(BoundingBox(Point(0,0),Point(self.width,self.height)),1)
        self.rockSize = 5
        self.win = GraphWin("MoveRocks", self.width, self.height)
        self.boxes = []
        self.rocks = []

        xWalls = [0,self.width]
        yWalls = [0,self.height]

        for i in range(self.numRocks):
            #click = self.win.getMouse() # Pause to view result

            startX = random.randint(0+self.rockSize,int(self.width)-self.rockSize)
            startY = random.randint(0+self.rockSize,int(self.height)-self.rockSize)

            speed = random.choice(self.rockSpeeds)

            self.rocks.append(Rock(Point(startX,startY),self.rockSize))

        self.win.flush()
        self.drawRocks()

        for i in range(1000):

            #time.sleep(.01)
            self.moveRocks()

        self.win.promptClose(self.win.getWidth()/2, 20)

    def drawRocks(self):
        for r in self.rocks:
            r.draw(self.win)

    def moveRocks(self):
        for r in self.rocks:
            r.move(r.dx(),r.dy())
            self.win.flush()

    def drawBoxes(self):
        boxes = self.q.getBBoxes()
        for box in boxes:
            box = Rectangle(box.ul,box.lr)
            box.draw(self.win)


if __name__ == '__main__':
    D = Driver(500,500)
