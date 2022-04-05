import math
from random import choice


class Point(object):
    """
    class Point:

        A point identified by (x,y) coordinates.

    @operations: +, -, *, /, str, repr
    @method: length         -- calculate length of vector to point from origin
    @method: distanceTo     -- calculate distance between two points
    @method: asTuple        -- construct tuple (x,y)
    @method: clone          -- construct a duplicate
    @method: castInt        -- convert x & y to integers
    @method: castFloat      -- convert x & y to floats
    @method: jumpTo         -- reset x & y
    @method: gotoPoint      -- move (in place) +dx, +dy, as spec'd by point
    @method: shiftDxDy      -- move (in place) +dx, +dy
    @method: rotate         -- rotate around the origin
    @method: rotateAbout    -- rotate around another point

    source: https://wiki.python.org/moin/PointsAndRectangles
    """

    def __init__(self, *args, **kwargs):

        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            self.x = kwargs.get("x", 0.0)
            self.y = kwargs.get("y", 0.0)

        self.data = kwargs.get("data", {})

    def __add__(self, p):
        """
        @returns Point(x1+x2, y1+y2)
        """
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        """
        @returns Point(x1-x2, y1-y2)
        """
        return Point(self.x - p.x, self.y - p.y)

    def __mul__(self, scalar):
        """
        Point(x1*x2, y1*y2)
        """
        return Point(self.x * float(scalar), self.y * float(scalar))

    def __div__(self, scalar):
        """
        Point(x1/x2, y1/y2)
        """
        return Point(self.x / scalar, self.y / scalar)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(x:{self.x} y:{self.y} data:{self.data})"

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # def setDxDy(self, dx, dy):
    #     """
    #     Change the speed of movement
    #     """
    #     self.dx = dx
    #     self.dy = dy

    def distanceTo(self, other):
        """Calculate the distance between two points.
        Params:
            other (Point)
        Returns:
            distance (float)
        """
        return (self - other).length()

    def asTuple(self):
        """Pull out x and y
        Params:
            other (Point)
        Returns:
            (x,y) (tuple)
        """
        return (self.x, self.y)

    def clone(self):
        """Return a full copy of this point.
        Params:
            None
        Returns:
            self (Point)
        """
        return Point(x=self.x, y=self.y)

    def castInt(self):
        """Convert co-ordinate values to integers
        Params:
            None
        Returns:
            None
        """
        self.x = int(self.x)
        self.y = int(self.y)

    def castFloat(self):
        """Convert co-ordinate values to floats
        Params:
            None
        Returns:
            None
        """
        self.x = float(self.x)
        self.y = float(self.y)

    def jumpTo(self, x, y):
        """Jumps to new position.
        Params:
            x (int)
            y (int)
        Returns:
            None
        """
        self.x = x
        self.y = y

    def gotoPoint(self, other):
        """Add points coords to current coords.
        Params:
            other (Point)
        Returns:
            None
        """
        self.x = self.x + other.x
        self.y = self.y + other.y

    def shiftDxDy(self, dx, dy):
        """Shift by dx and dy (x+dx,y+dy).
        Params:
            dx (int)
            dy (int)
        Returns:
            None
        """
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
        x, y = (c * self.x - s * self.y, s * self.x + c * self.y)
        return Point(x=x, y=y)

    def rotateAbout(self, p, theta):
        """
        Rotate counter-clockwise around a point, by theta degrees.

        Positive y goes *up,* as in traditional mathematics.

        The new position is returned as a new Point.
        """
        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
        result.slide(p.x, p.y)
        return result


if __name__ == "__main__":
    p1 = Point()
    print(p1)
    p2 = Point(5, 7)
    print(p2)
    p3 = Point(x=3, y=4)
    print(p3)
    p4 = p3 + p2
    print(p4)
    p1 = p4 * 3
    print(p1)
    p1.gotoPoint(Point(x=2, y=2))
    print(p1)
