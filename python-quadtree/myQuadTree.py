import math
import pantograph
import random
import numpy as np

"""
class Point:

    A point identified by (x,y) coordinates.

@operations: +, -, *, /, str, repr
@method: length         -- calculate length of vector to point from origin
@method: distance_to    -- calculate distance between two points
@method: as_tuple       -- construct tuple (x,y)
@method: clone          -- construct a duplicate
@method: integerize     -- convert x & y to integers
@method: floatize       -- convert x & y to floats
@method: move_to        -- reset x & y
@method: goto_point     -- move (in place) +dx, +dy, as spec'd by point
@method: move_to_xy     -- move (in place) +dx, +dy
@method: rotate         -- rotate around the origin
@method: rotate_about   -- rotate around another point
"""
class Point(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    """
    @returns Point(x1+x2, y1+y2)
    """
    def __add__(self, p):
        return Point(self.x+p.x, self.y+p.y)

    """
    @returns Point(x1-x2, y1-y2)
    """
    def __sub__(self, p):
        return Point(self.x-p.x, self.y-p.y)

    """
    Point(x1*x2, y1*y2)
    """
    def __mul__( self, scalar ):
        return Point(self.x*scalar, self.y*scalar)

    """
    Point(x1/x2, y1/y2)
    """
    def __div__(self, scalar):
        return Point(self.x/scalar, self.y/scalar)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    """
    Calculate the distance between two points.
    @returns distance
    """
    def distance_to(self, p):
        return (self - p).length()

    """
    @returns a tuple (x, y)
    """
    def as_tuple(self):
        return (self.x, self.y)

    """
    Return a full copy of this point.
    """
    def clone(self):
        return Point(self.x, self.y)

    """
    Convert co-ordinate values to integers.
    @returns Point(int(x),int(y))
    """
    def integerize(self):
        self.x = int(self.x)
        self.y = int(self.y)

    """
    Convert co-ordinate values to floats.
    @returns Point(float(x),float(y))
    """
    def floatize(self):
        self.x = float(self.x)
        self.y = float(self.y)

    """
    Moves / sets point to x,y .
    """
    def move_to(self, x, y):
        self.x = x
        self.y = y

    """
    Move to new (x+dx,y+dy).
    """
    def goto_point(self, p):
        self.x = self.x + p.x
        self.y = self.y + p.y

    """
    Move to new (x+dx,y+dy).
    """
    def move_to_xy(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    """
    Rotate counter-clockwise by rad radians.

    Positive y goes *up,* as in traditional mathematics.

    Interestingly, you can use this in y-down computer graphics, if
    you just remember that it turns clockwise, rather than
    counter-clockwise.

    The new position is returned as a new Point.
    """
    def rotate(self, rad):
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
        return Point(x,y)

    """
    Rotate counter-clockwise around a point, by theta degrees.

    Positive y goes *up,* as in traditional mathematics.

    The new position is returned as a new Point.
    """
    def rotate_about(self, p, theta):

        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
        result.slide(p.x, p.y)
        return result

    def set_direction(self,direction):
        assert direction in ['N','NE','E','SE','S','SW','W','NW']

        self.direction = direction

    def update_position(self):
        if self.direction == "N":
            self.y -= 1
        if self.direction == "NE":
            self.y -= 1
            self.x += 1
        if self.direction == "E":
            self.x += 1
        if self.direction == "SE":
            self.x += 1
            self.y += 1
        if self.direction == "S":
            self.y += 1
        if self.direction == "SW":
            self.x -= 1
            self.y += 1
        if self.direction == "W":
            self.x -= 1
        if self.direction == "NW":
            self.y -= 1
            self.x -= 1

class Rock(object):
    def __init__(self,start,speed,dest):
        self.start = start
        self.current = start
        self.speed = math.sqrt(speed)
        self.dest = dest
        self._calc_vector()
        self.size = 5

    def _calc_vector(self):
        self.distance = [self.start.x - self.dest.x, self.start.y - self.dest.y]
        self.norm = math.sqrt(self.distance[0]**2 + self.distance[1]**2)
        self.direction = [self.distance[0]/self.norm , self.distance[1]/self.norm ]
        self.vector = [self.direction[0]*self.speed, self.direction[1]*self.speed]

    def new_dest(self,dest):
        self.dest = dest
        self._calc_vector()

    def set_size(self,size):
        self.size = size

    def move_rock(self):
        self.current.x += self.vector[0]
        self.current.y += self.vector[1]


"""
Class Rect:
    A rectangle identified by two points.

    The rectangle stores left, top, right, and bottom values.

    Coordinates are based on screen coordinates.

    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom

@method: set_points     -- reset rectangle coordinates
@method: contains       -- is a point inside?
@method: overlaps       -- does a rectangle overlap?
@method: top_left       -- get top-left corner
@method: bottom_right   -- get bottom-right corner
@method: expanded_by    -- grow (or shrink)
"""
class Rectangle:

    """
    Initialize a rectangle from two points.
    """
    def __init__(self, pt1, pt2,data=None):
        self.set_points(pt1, pt2)
        self.w = math.abs(pt1.x-pt2.x)
        self.h = math.abs(pt1.y-pt2.y)
        self.data = data
        self.parent = None

    """
    Reset the rectangle coordinates.
    """
    def set_points(self, pt1, pt2):
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)

    """
    Return true if a point is inside the rectangle.
    """
    def contains(self, pt):
        x,y = pt.as_tuple()
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    """
    Return true if a rectangle overlaps this rectangle.
    """
    def overlaps(self, other):
        return (self.right > other.left and self.left < other.right and
                self.top < other.bottom and self.bottom > other.top)

    """
    Return the top-left corner as a Point.
    """
    def top_left(self):
        return Point(self.left, self.top)

    """
    Return the bottom-right corner as a Point.
    """
    def bottom_right(self):
        return Point(self.right, self.bottom)

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
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top,self.right,self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,Point(self.left, self.top),Point(self.right, self.bottom))


class collisionDetection(pantograph.PantographHandler):
    def setup(self):
        self.ptSize = 7
        self.rocks = []
        self.rockSpeeds = np.arange(.5,5,.5)
        self.numRocks = 300

        seqX = [0,self.width]
        seqY = [0,self.height]

        for i in range(self.numRocks):
            startX = random.randint(int(self.width/4),int(self.width/2))
            startY = random.randint(int(self.width/4),int(self.height/2))

            destX = random.choice(seqX)
            destY = random.choice(seqY)
            speed = random.choice(self.rockSpeeds)

            self.rocks.append(Rock(Point(startX,startY),speed,Point(destX,destY)))

        self.drawShapes()

    def drange(self,start, stop, step):
        r = start
        while r < stop:
            yield r
            r += step

    def moveShapes(self):
        for r in self.rocks:
            r.move_rock()


    def drawShapes(self):
        for r in self.rocks:
            self.fill_oval(r.current.x, r.current.y, r.size, r.size,"#F00")


    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        # draw the circle for the "rim" of the wheel
        self.drawShapes()
        self.moveShapes()

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(collisionDetection)
    app.run()
