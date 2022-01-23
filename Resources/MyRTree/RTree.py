import math
import random
import sys
import pantograph


ids = [chr(i) for i in range(65,65+26)]
cid =  -1

def getNextId():
    global ids
    global cid
    cid += 1
    if cid > 25:
        cid = cid % 26
    return ids[cid]

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

    """A rectangle identified by two points. The rectangle stores left, top, right, and bottom values.
    Coordinates are based on screen coordinates.

    y increases                                top
       /\                                       |
       |                                 left  -+-  right
       |                                        |
       +-----> x increases                    bottom
    origin

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
        top = min(self.top,other.top)
        right = max(self.right,other.right)
        bottom = max(self.bottom,other.bottom)
        return ( math.fabs(left-right) * math.fabs(top-bottom) )

    def merge(self,other):
        if self.area() == 0:
            self.left = other.left
            self.right = other.right
            self.top = other.top
            self.bottom = other.bottom
        else:
            self.left = min(self.left,other.left)
            self.top = min(self.top,other.top)
            self.right = max(self.right,other.right)
            self.bottom = max(self.bottom,other.bottom)
        self.width = math.fabs(self.left-self.right)
        self.height = math.fabs(self.top-self.bottom)

    def set_points(self, pt1, pt2):
        """Reset the rectangle coordinates."""
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)
        self.width = math.fabs(self.left-self.right)
        self.height = math.fabs(self.top-self.bottom)

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
                    self.top <= other.top and
                    self.bottom >= other.bottom)


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


class RandomData(object):
    def __init__(self,lb,ub,divisor=1,max_area=None):
        self.Points = []
        self.lowerBound = lb
        self.upperBound = ub
        self.divisor = divisor
        self.maxArea = max_area
    """

    """
    def randRect(self,x=None,y=None):

        r = Rect(self.randPoint(),self.randPoint())

        while r.area() > self.maxArea:
            self.Points.remove(r.top)
            self.Points.remove(r.bottom)
            self.Points.remove(r.left)
            self.Points.remove(r.right)
            r = Rect(self.randPoint(),self.randPoint())

        return r

    """

    """
    def randSquare(self,minw=0,maxw=0):

        lb = math.floor(math.sqrt(self.maxArea)*.20)
        ub = math.floor(math.sqrt(self.maxArea)*.90)

        if minw > 0 and maxw > 0:
            w = random.randrange(minw,maxw)
        else:
            w = random.randrange(lb,ub)

        x = self.randInt() - w
        y = self.randInt() - w

        p1 = Point(x,y)
        p2 = Point(x+w,y+w)
        r = Rect(p1,p2)

        # while w*w > self.maxArea:
        #     x = self.randInt()
        #     y = self.randInt()
        #     if minw > 0 and maxw > 0:
        #         w = random.randrange(minw,maxw)
        #     else:
        #         w = random.randrange(lb,ub)
        #     p1 = Point(x,y)
        #     p2 = Point(x+w,y+w)
        #     r = Rect(p1,p2)
        #     print (r)

        return r

    """

    """
    def randPoint(self):

        rx = self.randInt()
        ry = self.randInt()

        return Point(rx,ry)

    """

    """
    def randInt(self):
        attempts = 0

        ub = self.upperBound // self.divisor

        temp = (random.randrange(self.lowerBound,ub) * self.divisor)

        while temp in self.Points:
            temp = (random.randrange(self.lowerBound,ub) * self.divisor)
            attempts += 1
            if attempts > 1000:
                temp = self.divisor
                for i in range(self.upperBound,self.divisor):
                    if not i in self.Points:
                        temp = i
                        break

        self.Points.append(temp)

        return temp




class Node(object):
    def __init__(self,M,leaf=True):
        self.id = getNextId()
        self.M = M
        self.m = M // 2
        self.Children = []
        self.Parent = None
        self.Bbox = Rect()
        self.Leaf = leaf
        self.color = self.randomColor()

    def __repr__(self):
        if "bbox" in dir(self.Parent):
            parent = self.Parent.bbox
        else:
            parent = None
        #return "\nM: %s\tParent: %s\tChildren: %s\tBbox: %s\n" % (self.M,self.Parent,self.Children,self.Bbox)
        return f"{self.id} M:{self.M} Parent:{self.Parent} Children{self.Children} BBox{self.Bbox}"

    def randomColor(self):
        r = lambda: random.randint(0,255)
        return ('#%02X%02X%02X' % (r(),r(),r()))

    """
    Add rectangle item to Node
    Resize bounding rectangle
    """
    def insert(self,R,parent=None):
        self.Children.append(R)
        if isinstance(R, Rect):
            self.Bbox.merge(R)
        else:
            self.Bbox.merge(R.Bbox)

        if len(self.Children) > self.M:
            return self.splitNode(self.id)

        # print("children>>>")
        # print(self.Children)
        # print("<<<<children")

        return None

    """
    Remove rectangle item from Node
    Resize bounding rectangle
    """
    def remove(self,R):
        self.Children.remove(R)
        self.Bbox = Rect()
        for i in self.Children:
            self.Bbox.merge(i)


    def splitNode(self,id=None):
        L = Node(self.M)
        LL = Node(self.M)

        R1,R2 = self.pickSeeds()    # Pick two rectangles

        L.insert(R1)
        LL.insert(R2)

        self.remove(R1)
        self.remove(R2)

        while self.Children:
            R = self.pickNext(L,LL)

            if R == 0:
                return
            d1 = math.fabs(L.Bbox.potential_area(R) - L.Bbox.area())
            d2 = math.fabs(LL.Bbox.potential_area(R) - LL.Bbox.area())

            """ Add it to the group whose covering rectangle will have to be enlarged least to accommodate it. """
            if d1 < d2:
                L.insert(R)
            else:
                LL.insert(R)

            self.remove(R)

        # I wanted to just do self = L , but obviously that wont work with a local var
        # Little wasteful

        for R in L.Children:
            self.insert(R)

        return LL

    """
    Select one remaining entry for classification in a group.
    Find entry with greatest preference for one group.
    Choose the entry with the maximum difference between d1 and d2.
    """
    def pickNext(self,L,LL):

        maxDiff = 0
        C = 0
        for c in self.Children:
            diff = math.fabs(L.Bbox.potential_area(c) - LL.Bbox.potential_area(c))

            if diff > maxDiff:
                maxDiff = diff
                C = c

        return C

    """
    Select two entries to be the first elements of the groups.
    Choose the most wasteful pair.
    """
    def pickSeeds(self):

        R1 = None
        R2 = None

        d = 0
        l = len(self.Children)

        if l == 2:
            return (self.Children[0],self.Children[1])

        if l == 3:
            return (self.Children[0],self.Children[2])

        for i in range(l):
            for j in range(l):
                if i == j:
                    continue
                J = self.Children[i].potential_area(self.Children[j])
                temp = J - self.Children[i].area() - self.Children[j].area()
                if temp > d:
                    R1 = self.Children[i]
                    R2 = self.Children[j]
                    d = temp
                if R1 == None:
                    R1 = self.Children[i]
                if R2 == None:
                    R2 = self.Children[j]
        return (R1,R2)



class printRtree(pantograph.PantographHandler):

    def setup(self):

        self.N = []
        self.N.append(Node(3))
        self.Rd = RandomData(5,self.width,10,2000)

    def addRectangle(self,x=None,y=None):

        if x and y:
            p1 = Point(x,y)
            p2 = Point(x+random.randint(10,30),y+random.randint(10,30))
            r = Rect(p1,p2)
        else:
            r = self.Rd.randRect()
            #r = self.Rd.randSquare(50,150)
        print(r)

        L = self.chooseLeaf(r)

        LL = L.insert(r)

        if LL:
            self.N.append(LL)

        print ("==============")
        for n in self.N:
            print (n)

    def showTestRects(self):
        test = [Point(39,21),Point(86,19),Point(65,5),Point(76,28),Point(3,9),Point(31,59),Point(43,99),Point(60,50),Point(42,48),Point(15,73),Point(67,98),Point(16,34),Point(27,80),Point(51,77),Point(30,67),Point(82,68),Point(85,46),Point(89,44),Point(21,30),Point(5,66),Point(75,29),Point(17,14),Point(40,90),Point(18,33),Point(52,64),Point(1,71),Point(88,10),Point(64,26),Point(96,2),Point(25,40)]

        s = 0
        while len(test) > 0:
            p1 = test.pop(0)
            p2 = test.pop(0)
            p1.x *= 5
            p1.y *= 5
            p2.x *= 5
            p2.y *= 5

            r = Rect(p1,p2)
            # print(r)

            L = self.chooseLeaf(r)

            # print(L)

            LL = L.insert(r)

            if LL:
                self.N.append(LL)
            s += 1
            # if s == 4:
            #     break

    def drawRectangles(self):
        for n in self.N:
            self.dashedRect(n.Bbox.top_left(),n.Bbox.bottom_right(),10)
            #self.draw_rect(n.Bbox.left, n.Bbox.top, n.Bbox.width, n.Bbox.height,"#000")
            for c in n.Children:
                self.draw_rect(c.left, c.top, c.width, c.height,n.color)

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        #self.showTestRects()
        self.drawRectangles()
        #self.draw_image("A.png", 5, 5)

    def chooseLeaf(self,R):

        if len(self.N) == 1:
            return self.N[0]

        minimum = int(pow(2,30))
        #print(minimum)
        F = None
        #print(R)
        for n in self.N:
            #print(n)
            #print(n.Bbox.potential_area(R))
            if n.Bbox.potential_area(R) < minimum:
                minimum = n.Bbox.potential_area(R)
                #print(minimum)
                F = n
        return F

    def on_mouse_down(self,InputEvent):
        self.addRectangle(InputEvent.x,InputEvent.y)
        print(InputEvent.x,InputEvent.y)
        printRTree(self.N)

    def randomColor(self):
        r = lambda: random.randint(200,255)
        return ('#%02X%02X%02X' % (r(),r(),r()))

    def dashedRect(self,start,stop,step):
        startX = start.x
        startY = start.y
        stopX = stop.x
        stopY = stop.y

        for sx in range(startX,stopX,step*2):
            if sx + step > stopX:
                break
            self.draw_line(sx, startY, sx+step, startY, "#c0c0c0")

        for sx in range(startX,stopX,step*2):
            if sx + step > stopX:
                break
            self.draw_line(sx, stopY, sx+step, stopY, "#c0c0c0")

        for sy in range(startY,stopY,step*2):
            if sy + step > stopY:
                break
            self.draw_line(startX, sy, startX, sy+step, "#c0c0c0")

        for sy in range(startY,stopY,step*2):
            if sy + step > stopY:
                break
            self.draw_line(stopX, sy, stopX, sy+step, "#c0c0c0")

def printRTree(root):
    for i in root:
        if isinstance(i, Node):
            print (i)
            printRTree(i.Children)


if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(printRtree)
    app.run()
