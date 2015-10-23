import math
from Point import Point


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
    def __init__(self, pt1=None, pt2=None,data=None):
        if not pt1:
            pt1 = Point()
        if not pt2:
            pt2 = Point()

        self.set_points(pt1, pt2)
        self.w = math.fabs(pt1.x-pt2.x)
        self.h = math.fabs(pt1.y-pt2.y)
        self.data = data
        self.parent = None

    """
    Reset the rectangle coordinates.
    """
    def set_points(self, pt1, pt2):
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)
        self.w = math.fabs(pt1.x-pt2.x)
        self.h = math.fabs(pt1.y-pt2.y)
        self.center = Point((math.fabs(x1-x2)/2),(math.fabs(y1-y2)/2))

    """
    Return true if a point is inside the rectangle.
    """
    def contains(self, pt):
        x,y = pt.as_tuple()
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    """
    Return true if a rect is inside this rectangle.
    """
    def encompasses(self, other):
        return  (self.left <= other.left and
                self.right >= other.right and
                self.top <= other.top and
                self.bottom >= other.bottom)

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


if __name__ == '__main__':
    rect = Rectangle()
    print rect
