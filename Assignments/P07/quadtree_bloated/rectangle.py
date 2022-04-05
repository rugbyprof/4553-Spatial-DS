import math
from point import Point


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

source: https://wiki.python.org/moin/PointsAndRectangles
"""


class Rectangle:
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            self.p1 = args[0]
            self.p2 = args[1]
        else:
            self.p1 = kwargs.get("p1", Point())
            self.p2 = kwargs.get("p2", Point())

        self.data = kwargs.get("data", {})
        self.parent = kwargs.get("parent", None)
        self.color = kwargs.get("color", (0, 0, 0))

        self.setPoints(self.p1, self.p2)
        self.w = math.fabs(self.p1.x - self.p2.x)
        self.h = math.fabs(self.p1.y - self.p2.y)

    def setPoints(self, p1, p2):
        """Reset the rectangle coordinates."""
        (x1, y1) = p1.asTuple()
        (x2, y2) = p2.asTuple()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)
        self.w = math.fabs(p1.x - p2.x)
        self.h = math.fabs(p1.y - p2.y)
        self.center = Point((math.fabs(x1 - x2) / 2), (math.fabs(y1 - y2) / 2))

    def contains(self, pt):
        """Return true if a point is inside the rectangle.
        Params:
            pt (Point)
        Returns:
            bool : True = does contain
        """
        x, y = pt.asTuple()
        # print(
        #     f"{self.left} <= {x} and {x} <= {self.right} and {self.top} <= {y} and {y} <= {self.bottom}"
        # )
        # print(self.left <= x and x <= self.right and self.top <= y and y <= self.bottom)
        return self.left <= x and x <= self.right and self.top <= y and y <= self.bottom

    def encompasses(self, rect):
        """
        Return true if a rect is inside this rectangle.
        Params:
            rect (Rectangle)
        Returns:
            bool : True = does encompass
        """
        return (
            self.left <= rect.left
            and self.right >= rect.right
            and self.top <= rect.top
            and self.bottom >= rect.bottom
        )

    def overlaps(self, rect):
        """Return true if a rectangle overlaps this rectangle.
        Params:
            rect (Rectangle)
        Returns:
            bool : True = does encompass
        """
        return (
            self.right > rect.left
            and self.left < rect.right
            and self.top < rect.bottom
            and self.bottom > rect.top
        )

    def topLeft(self):
        """
        Return the top-left corner as a Point.
        """
        return Point(self.left, self.top)

    def bottomRight(self):
        """
        Return the bottom-right corner as a Point.
        """
        return Point(self.right, self.bottom)

    def expandedBy(self, scalar):
        """Return a rectangle with extended borders.
            Create a new rectangle that is wider and taller than thecimmediate one.
            All sides are extended by "n" points.
        Params:
            scalar (int)
        Returns:
            Rectangle
        """
        p1 = Point(self.left - scalar, self.top - scalar)
        p2 = Point(self.right + scalar, self.bottom + scalar)
        return Rectangle(p1, p2)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):

        s = "( "
        s += f"  {self.__class__.__name__}("
        s += f"  {Point(self.left, self.top)} , "
        s += f"  {Point(self.right, self.bottom)}"
        s += " )"
        return s


class Bounds(object):
    """
    A class more or so to put all the boundary values together. Friendlier than
    using a map type.
    """

    def __init__(self, minx, miny, maxx, maxy):
        self.minX = minx
        self.minY = miny
        self.maxX = maxx
        self.maxY = maxy

    def __repr__(self):
        return f"({self.minX}, {self.minY}, {self.maxX}, {self.maxY})"


if __name__ == "__main__":
    rect = Rectangle(p1=Point(2, 2), p2=Point(4, 4))
    print(rect)
