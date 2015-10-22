import math
import random
import sys

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

    def rotate_about(self, p, theta):
        """Rotate counter-clockwise around a point, by theta degrees.

        Positive y goes *up,* as in traditional mathematics.

        The new position is returned as a new Point.
        """
        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
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

    def __init__(self, pt1=None, pt2=None):
        """Initialize a rectangle from two points."""
        if not pt1:
            pt1 = Point(0,0)
        if not pt2:
            pt2 = Point(0,0)
        self.set_points(pt1, pt2)

    def area(self):
        return ( math.fabs(self.left-self.right) * math.fabs(self.top-self.bottom) )

    def potential_area(self,other):
        left = min(self.left,other.left)
        top = max(self.top,other.top)
        right = max(self.right,other.right)
        bottom = min(self.bottom,other.bottom)
        return ( math.fabs(left-right) * math.fabs(top-bottom) )

    def merge(self,other):
        if self.area() == 0:
            self.left = other.left
            self.right = other.right
            self.top = other.top
            self.bottom = other.bottom
        else:
            self.left = min(self.left,other.left)
            self.top = max(self.top,other.top)
            self.right = max(self.right,other.right)
            self.bottom = min(self.bottom,other.bottom)

    def set_points(self, pt1, pt2):
        """Reset the rectangle coordinates."""
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = max(y1, y2)
        self.right = max(x1, x2)
        self.bottom = min(y1, y2)

    """Return true if other is inside the rectangle."""
    def contains(self, other):

        assert isinstance(other, Point) or isinstance(other, Rect), "contains requires a Point or Rect"

        if isinstance(other, Point):
            x,y = other.as_tuple()
            return (self.left <= x <= self.right and
                    self.top <= y <= self.bottom)

        if isinstance(other,Rect):
            return (self.left <= other.left and
                    self.right >= other.right and
                    self.top >= other.top and
                    self.bottom <= other.bottom)


    def overlaps(self, other):
        """Return true if a rectangle overlaps this rectangle."""
        return (self.right > other.left and self.left < other.right and
                self.top > other.bottom and self.bottom < other.top)

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
        p1 = Point(self.left-n, self.top+n)
        p2 = Point(self.right+n, self.bottom-n)
        return Rect(p1, p2)

    def __str__( self ):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top,
                                           self.right,self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,
                               Point(self.left, self.top),
                               Point(self.right, self.bottom))


class Node(object):
    def __init__(self,M,leaf=True):
        self.M = M
        self.P = None               # Parent pointer
        self.I = []                 # Container of boxes or node pointers
        self.bbox = Rect()          # Bounding box that holds all children
        self.Leaf = leaf

    def __repr__(self):
        return "\nM: %s\nP: %s\nI: %s\nbbox: %s\n" % (self.M,self.P,self.I,self.bbox)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def splitMe(self):
        return len(self.I) > self.M

    """
    Add rectangle item to Node
    Resize bounding rectangle
    """
    def install(self,E):
        self.I.append(E)
        if isinstance(E, Rect):
            self.bbox.merge(E)
        else:
            self.bbox.merge(E.bbox)

    """
    Remove rectangle item from Node
    Resize bounding rectangle
    """
    def uninstall(self,E):
        self.I.remove(E)
        self.bbox = Rect()
        for i in self.I:
            self.bbox.merge(i)

    # If the items in "I" are Nodes, then it has children and is NOT a leaf
    def isLeaf(self):
        for i in self.I:
            if isinstance(i, Node):
                return False
        return True

    def length(self):
        return len(self.I)


    """
    Select two entries to be the first elements of the groups.
    Choose the most wasteful pair.
    """
    def pickSeeds(self):

        d = 0
        l = len(self.I)

        for i in range(l):
            for j in range(l):
                if i == j:
                    continue
                J = self.I[i].potential_area(self.I[j])
                temp = J - self.I[i].area() - self.I[j].area()
                if temp > d:
                    E1 = self.I[i]
                    E2 = self.I[j]
                    d = temp
        return (E1,E2)

    """
    Select one remaining entry for classification in a group.
    Find entry with greatest preference for one group.
    Choose the entry with the maximum difference between d1 and d2.
    """
    def pickNext(self,L,LL):

        maxDiff = 0
        for e in self.I:
            diff = math.fabs(L.bbox.potential_area(e) - LL.bbox.potential_area(e))

            if diff > maxDiff:
                maxDiff = diff
                E = e

        return E


    def splitNode(self):
        L = Node(self.M)
        LL = Node(self.M)

        E1,E2 = self.pickSeeds()

        L.install(E1)
        LL.install(E2)
        self.uninstall(E1)
        self.uninstall(E2)

        while self.I:
            E = self.pickNext(L,LL)

            d1 = math.fabs(L.bbox.potential_area(E) - L.bbox.area())
            d2 = math.fabs(LL.bbox.potential_area(E) - LL.bbox.area())

            """ Add it to the group whose covering rectangle will have to be enlarged least to accommodate it. """
            if d1 < d2:
                L.install(E)
            else:
                LL.install(E)

            self.uninstall(E)

        # I wanted to just do self = L , but obviously that wont work with a local var
        # Little wasteful

        for E in L.I:
            self.install(E)

        return LL


class RTree(object):
    def __init__(self,M):
        self.M = M
        self.m = M // 2
        self.root = Node(self.M,False)


    def __repr__(self):
        return "\nM: %s\nm: %s\nroot: %s\n" % (self.M,self.m,self.root)

    def adjustTree(self,L,LL):
        N = L
        NN = LL

        split = isinstance(NN, Node)    # otherwise it would be NONE
        done = (N == self.root)

        """ If at the root """
        if done:
            """ If there was a split """
            if split:
                """ Grow tree up """
                self.root = Node(self.M,False)
                self.root.install(N)
                self.root.install(NN)
                N.P = self.root
                NN.P = self.root
        else:
            N.P.bbox.merge(N.bbox)
            if split:
                N.P.install(NN)
                N.P.bbox.merge(NN.bbox)
                if N.P.splitMe():
                    NN = N.P.splitNode()
                else:
                    NN = None
            self.adjustTree(N.P,NN)


    def condenseTree(self):
        pass

    def chooseLeaf(self,N,E):
        if N.isLeaf():
            return N
        else:
            minimum = sys.maxint
            F = None
            for n in N.I:
                if n.bbox.potential_area(E) < minimum:
                    minimum = n.bbox.potential_area(E)
                    F = n
            return F


    def findLeaf(self):
        pass

    def insert(self,E):
        assert isinstance(E, Rect), "RTree insert requires a Rect type."

        LL = None   # LL is only needed if we split

        L = self.chooseLeaf(self.root,E)

        """ if L is root we create a leaf node and attach """
        if L == self.root:
            N = Node(self.M)
            N.install(E)
            N.P = L
            L.install(N)
        else:
            L.install(E)

        if L.splitMe():
            LL = L.splitNode()

        self.adjustTree(L,LL)

    def traverseTree(self):
        self._traverse(self.root,0)

    def _traverse(self,root,level):
        tabs = ""
        for i in range(level):
            tabs = tabs + "\t"

        if root.isLeaf():
            print "%sLeaf @ level: %s" % (tabs,level)
            print "%s%s" % (tabs,root.I)
        else:
            for n in root.I:
                print "%sInnernode @ level: %s" % (tabs,level)
                print "%s%s" % (tabs,root.bbox)
                self._traverse(n,level+1)

"""
Generate a random rectangle with coordinates divisible by "divisor" (e.g. 5 or 10)
for easy debugging
"""
def randRect(lb,ub,divisor,max_area=None):

    ub = ub // divisor
    p = []
    if max_area == None:
        max_area = sys.maxint

    for i in range(4):
        p.append(random.randrange(lb,ub) * divisor)

    R = Rect(Point(p[0],p[1]),Point(p[2],p[3]))

    while R.area() > max_area or p[0] == p[2] or p[1] == p[3]:
        for i in range(4):
            p[i] = random.randrange(lb,ub) * divisor

        R = Rect(Point(p[0],p[1]),Point(p[2],p[3]))

    return R

def randPoint(lb,ub):

    x = []
    y = []

    for i in range(30):

        rx = random.randrange(lb,ub)
        ry = random.randrange(lb,ub)

        while rx in x:
            rx = random.randrange(lb,ub)
        while ry in y:
            ry = random.randrange(lb,ub)

        x.append(rx)
        y.append(ry)

    return zip(x,y)

if __name__=='__main__':
    #random.seed(91283764)
    random.seed(8768)

    M = 5

    R = RTree(M)

    #for i in range(11):
    #    R.insert(randRect(1,100,5,200))

    #R.traverseTree()

    #print len(R.root.I)

    print randPoint(1,100)
