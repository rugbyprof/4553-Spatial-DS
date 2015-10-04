import math
from Point import Point

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
        return (self.ul.x <= p.x <= self.lr.x and self.ul.y <= p.y <= self.lr.y)
        #return (p.x > self.ul.x and p.x < self.lr.x and p.y > self.ul.y and p.y < self.lr.y)

    """
    Return true if a rect is inside this rectangle.
    """
    def containsBox(self, other):
        #print other.ul.x ,' > ', self.ul.x ,' and ', other.ul.y ,' > ', self.ul.y ,' and ' ,other.lr.x ,' < ', self.lr.x ,' and ', other.lr.y ,' < ', self.lr.y
        return (other.ul.x > self.ul.x and other.ul.y > self.ul.y and other.lr.x < self.lr.x and other.lr.y < self.lr.y)


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
        return "<Rect (ul.x:%s,ul.y:%s) , (lr.x:%s, lr.y:%s)>" % (self.ul.x,self.ul.y,self.lr.x,self.lr.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,Point(self.ul.x, self.ul.y),Point(self.lr.x, self.lr.y))


if __name__ == '__main__':
    rect = Rectangle()
    print rect
