import math
import random
import pantograph
import numpy as np
import sys
import itertools as IT

"""Point and Rectangle classes.

This code is in the public domain.

Point  -- point with (x,y) coordinates
Rect  -- two points, forming a rectangle
"""
class Point:

    """A point identified by (x,y) coordinates.

    supports: +, -, *, /, str, repr

    length  -- calculate length of vector to point from origin
    distance_to  -- calculate distance between two points
    as_tuple  -- construct tuple (x,y)
    clone  -- construct a duplicate
    integerize  -- convert x & y to integers
    floatize  -- convert x & y to floats
    move_to  -- reset x & y
    slide  -- move (in place) +dx, +dy, as spec'd by point
    slide_xy  -- move (in place) +dx, +dy
    rotate  -- rotate around the origin
    rotate_about  -- rotate around another point
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, p):
        """Point(x1+x2, y1+y2)"""
        return Point(self.x+p.x, self.y+p.y)

    def __sub__(self, p):
        """Point(x1-x2, y1-y2)"""
        return Point(self.x-p.x, self.y-p.y)

    def __mul__( self, scalar ):
        """Point(x1*x2, y1*y2)"""
        return Point(self.x*scalar, self.y*scalar)

    def __div__(self, scalar):
        """Point(x1/x2, y1/y2)"""
        return Point(self.x/scalar, self.y/scalar)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()

    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)

    def clone(self):
        """Return a full copy of this point."""
        return Point(self.x, self.y)

    def integerize(self):
        """Convert co-ordinate values to integers."""
        self.x = int(self.x)
        self.y = int(self.y)

    def floatize(self):
        """Convert co-ordinate values to floats."""
        self.x = float(self.x)
        self.y = float(self.y)

    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y

    def slide(self, p):
        '''Move to new (x+dx,y+dy).

        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + p.x
        self.y = self.y + p.y

    def slide_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy).

        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + dx
        self.y = self.y + dy

    def rotate(self, rad):
        """Rotate counter-clockwise by rad radians.

        Positive y goes *up,* as in traditional mathematics.

        Interestingly, you can use this in y-down computer graphics, if
        you just remember that it turns clockwise, rather than
        counter-clockwise.

        The new position is returned as a new Point.
        """
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
        return Point(x,y)

    def rotate_about(self, p, angle):
        """Rotate counter-clockwise around a point, by angle degrees.

        Positive y goes *up,* as in traditional mathematics.

        The new position is returned as a new Point.
        """
        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(angle)
        result.slide(p.x, p.y)
        return result


class Rect:

    """A rectangle identified by two points.

    The rectangle stores left, top, right, and bottom values.

    Coordinates are based on screen coordinates.

    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom

    set_points  -- reset rectangle coordinates
    contains  -- is a point inside?
    overlaps  -- does a rectangle overlap?
    top_left  -- get top-left corner
    bottom_right  -- get bottom-right corner
    expanded_by  -- grow (or shrink)
    """

    def __init__(self, pt1, pt2):
        """Initialize a rectangle from two points."""
        self.set_points(pt1, pt2)

    def set_points(self, pt1, pt2):
        """Reset the rectangle coordinates."""
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)

    def contains(self, pt):
        """Return true if a point is inside the rectangle."""
        x,y = pt.as_tuple()
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    def overlaps(self, other):
        """Return true if a rectangle overlaps this rectangle."""
        return (self.right > other.left and self.left < other.right and
                self.top < other.bottom and self.bottom > other.top)

    def top_left(self):
        """Return the top-left corner as a Point."""
        return Point(self.left, self.top)

    def bottom_right(self):
        """Return the bottom-right corner as a Point."""
        return Point(self.right, self.bottom)

    def expanded_by(self, n):
        """Return a rectangle with extended borders.

        Create a new rectangle that is wider and taller than the
        immediate one. All sides are extended by "n" points.
        """
        p1 = Point(self.left-n, self.top-n)
        p2 = Point(self.right+n, self.bottom+n)
        return Rect(p1, p2)

    def __str__( self ):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top,self.right,self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,Point(self.left, self.top),Point(self.right, self.bottom))

class Polygon:

    def __init__(self, pts=[],centroid=None):
        """Initialize a polygon from list of points."""

        self.set_points(pts,centroid)

    def set_points(self, pts,centroid=None ):
        """Reset the poly coordinates."""

        if not centroid == None:
            self.centroid = Point(centroid[0],centroid[1])

        self.minX = sys.maxint
        self.minY = sys.maxint
        self.maxX = sys.maxint * -1
        self.maxY = sys.maxint * -1

        self.points = []
        #self.mbr = Rect()
        for p in pts:
            x,y = p

            if x < self.minX:
                self.minX = x
            if x > self.maxX:
                self.maxX = x
            if y < self.minY:
                self.minY = y
            if y > self.maxY:
                self.maxY = y

            self.points.append(Point(x,y))

        self.mbr = Rect(Point(self.minX,self.minY),Point(self.maxX,self.maxY))

    def get_points(self):
        generic = []
        for p in self.points:
            generic.append(p.as_tuple())
        return generic

    # determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs.
    def point_inside_polygon(self, p):

        n = len(self.points)
        inside =False

        p1x,p1y = self.points[0].as_tuple()
        for i in range(n+1):
            p2x,p2y = self.points[i % n].as_tuple()
            if p.y > min(p1y,p2y):
                if p.y <= max(p1y,p2y):
                    if p.x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (p.y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or p.x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def orderPoints(self):
        assert not self.centroid == None

        ptsDict = {}
        for p in self.points:
            ptsDict[self.angleWithRespect2Centroid(p.x,p.y)] = p
            #print self.angleWithRespect2Centroid(p.x,p.y)
        self.points = []
        for key in sorted(ptsDict):
            #print "%s: %s" % (key, ptsDict[key])
            self.points.append(ptsDict[key])

    def calcArea(self,x, y):
        """Calculates the signed area of an arbitrary polygon given its verticies
        http://stackoverflow.com/a/4682656/190597 (Joe Kington)
        http://softsurfer.com/Archive/algorithm_0101/algorithm_0101.htm#2D%20Polygons
        """
        area = 0.0
        for i in xrange(-1, len(x) - 1):
            area += x[i] * (y[i + 1] - y[i - 1])
        return area / 2.0

    def calcCentroid(self):
        """
        http://stackoverflow.com/a/14115494/190597 (mgamba)
        """
        area = self.calcArea(*zip(*points))
        points = self.points
        result_x = 0
        result_y = 0
        N = len(points)
        points = IT.cycle(points)
        x1, y1 = next(points)
        for i in range(N):
            x0, y0 = x1, y1
            x1, y1 = next(points)
            cross = (x0 * y1) - (x1 * y0)
            result_x += (x0 + x1) * cross
            result_y += (y0 + y1) * cross
        result_x /= (area * 6.0)
        result_y /= (area * 6.0)
        return (result_x, result_y)

    def angleWithRespect2Centroid(self,x,y):
        assert not self.centroid == None

        return math.atan2(y - self.centroid.y, x - self.centroid.x)

    def __str__( self ):
        return "<Polygon \n Points: %s \n Mbr: %s \n Centroid: %s>" % ("".join(str(self.points)),str(self.mbr),str(self.centroid))

    def __repr__(self):
        return "%s %s" % (self.__class__.__name__,''.join(str(self.points)))

class RandPolygon(object):
    def __init__(self,minDist=100,maxDist=1000,minPoints=3,maxPoints=1000,startY=33.230073,startX=-97.143826):
        self.minDist = minDist
        self.maxDist = maxDist
        self.minPoints = minPoints
        self.maxPoints = maxPoints
        self.randPoints = random.randrange(self.minPoints,self.maxPoints)
        self.startX = startX
        self.startY = startY

        self.currIteration = 0.0
        self.maxIteration = self.maxPoints

        self.polygon = Polygon()
        self.points = []

        self.generatePolygon()

    def destination(self,x,y,angle, distance):
        """
        Displace a LatLng angle degrees counterclockwise and some
        meters in that direction.
        Notes:
            http://www.movable-type.co.uk/scripts/latlong.html
            0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
        Args:
            angle:    A number in degrees.
            distance: A number in meters.
        Returns:
            A new LatLng.
        """
        angle = np.float32(angle)

        delta = np.divide(np.float32(distance), np.float32(3959))

        angle = self.deg2rad(angle)
        y1 = self.deg2rad(y)
        x1 = self.deg2rad(x)

        y2 = np.arcsin( np.sin(y1) * np.cos(delta) +
                          np.cos(y1) * np.sin(delta) * np.cos(angle) )

        x2 = x1 + np.arctan2( np.sin(angle) * np.sin(delta) * np.cos(y1),
                                  np.cos(delta) - np.sin(y1) * np.sin(y2))

        x2 = (x2 + 3 * np.pi) % (2 * np.pi) - np.pi

        return [self.rad2deg(x2),self.rad2deg(y2)]

    def deg2rad(self,angle):
            return np.divide(np.dot(angle, np.pi), np.float32(180.0))

    def rad2deg(self,angle):
            return np.divide(np.dot(angle, np.float32(180.0)), np.pi)

    def generatePolygon(self):
        pts = []
        n = self.randPoints
        for i in range(n):
            angle = self.randAngle(i,n,"Degrees")
            distance = random.randrange(self.minDist,self.maxDist)
            #print angle,distance
            xy = self.destination(self.startX,self.startY,self.rad2deg(angle),distance)
            pts.append((xy[0],xy[1]))
            #print xy[1],",",xy[0],":",self.getPointAngle(xy[0],xy[1])
        self.polygon.set_points(pts,(self.startX,self.startY))
        self.polygon.orderPoints()
        pts = self.polygon.get_points()
        for p in pts:
            print p[1],",",p[0],":"


    def randDistance(self):
        random.randrange(self.minDist,self.maxDist)

    """
    @private
    @method - randAngle: Generates a random angle between the ith and ith + 1 iteration.
                         Meaning that if this function was called 4 times, it would successively
                         return angles: 0-90,90-180,180-270,270-360
    @param {int} i      : Current iteration count (or starting angle)
    @param {int} n      : Max iterations (or ending angle)
    @param {string}     : Radians or Degrees
    @returns list[]: list of items in node
    """
    def randAngle(self,i,n,Units="Radians"):
        i = float(i)
        n = float(n)
        value = (2.0 * math.pi) * random.uniform((i)/n , (i+1)/n)
        if Units == "Radians":
            return value
        else:
            return math.degrees(value)


if __name__ == '__main__':
    rp = RandPolygon(200,500,25,150,33.230073,-97.143826)
