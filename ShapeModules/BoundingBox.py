import math
from Point import Point

class BoundingBox(object):

    """
    Initialize a rectangle from two points.
    x1,y1 = upper LEFT
    x2,y2 = lower RIGHT
    """
    def __init__(self, pt1=None, pt2=None):
        if not pt1:
            pt1 = Point()
        if not pt2:
            pt2 = Point()

        self.set_points(pt1, pt2)
        self.parent = None

    """
    Reset the bbox coordinates.
    """
    def set_points(self, pt1, pt2):
        self.ul = pt1
        self.lr = pt2
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.w = math.fabs(pt1.x-pt2.x)
        self.h = math.fabs(pt1.y-pt2.y)
        self.center = Point((math.fabs(x1-x2)/2),(math.fabs(y1-y2)/2))


    """
    Return true if a point is inside the rectangle.
    """
    def containsPoint(self, p):
        x,y = p.as_tuple()

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


if __name__ == '__main__':
    rect = Rectangle()
    print rect
