import math

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

if __name__ == '__main__':
    p = Point()
    print p
