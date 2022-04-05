import math
from point import Point


class Vector(object):
    """A vector can be determined from a single point when basing
    it from the origin (0,0), but I'm going to assume 2 points.
    Example:
        AB = Vector(Point(3,4),Point(6,7))

    or if you want to use the origin

        AB = Vector(Point(0,0),Point(8,4))

    @method: _bearing       -- private method to give the bearing going from p1 -> p2
    @method: _magnitude     -- length in this context
    @method: _step          -- a "location change vector" (not correct term) to apply to point p1
                               that will "step" it towards p2. The size of the "step" is
                               based on the velocity.
    """

    def __init__(self, *args, **kwargs):

        if len(args) == 2:
            self.p1 = args[0]
            self.p2 = args[1]
        else:
            self.p1 = kwargs.get("p1", None)
            self.p2 = kwargs.get("p2", None)

        # error check for bad or missing stuff for p1 and p2

        self.velocity = kwargs.get("velocity", 1)
        self.dx = 0
        self.dy = 0

        self.v = [self.p1.x - self.p2.x, self.p1.y - self.p2.y]
        self.a = self.v[0]
        self.b = self.v[1]

        self.magnitude = self._magnitude()
        self.bearing = self._bearing()
        self.step = self._step()

    def _str__(self):
        return self.__repr__()

    def __repr__(self):
        d = self.tupleMe()
        s = self.__class__.__name__
        s += f"(\n  p1: {d[0][0]},{d[0][1]}\n  p2: {d[1][0]},{d[1][1]}\n"
        s += f"  v: {d[2]}\n  a: {d[3]}\n  b: {d[4]}\n  velocity: {d[5]}\n  bearing: {d[6]}\n"
        s += f"  magnitude: {d[7]}\n  step: {d[8]}\n)"
        return s

    def tupleMe(self):
        return (
            self.p1.asTuple(),
            self.p2.asTuple(),
            self.v,
            self.a,
            self.b,
            self.velocity,
            self.bearing,
            self.magnitude,
            self.step,
        )

    def _bearing(self):
        """Calculate the bearing (in radians) between p1 and p2"""
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        rads = math.atan2(-dy, dx)
        return rads % 2 * math.pi  # In radians
        # degs = degrees(rads)

    def _magnitude(self):
        """A vector by itself can have a magnitude when basing it on the origin (0,0),
        but in this context we want to calculate magnitude (length) based on another
        point (converted to a vector).
        """
        return math.sqrt((self.a ** 2) + (self.b ** 2))

    def _step(self):
        """Create the step factor between p1 and p2 to allow a point to
        move toward p2 at some interval based on velocity. Greater velocity
        means bigger steps (less granular).
        """
        cosa = math.sin(self.bearing)
        cosb = math.cos(self.bearing)
        self.dx = cosa * self.velocity
        self.dy = cosb * self.velocity
        return [cosa * self.velocity, cosb * self.velocity]


if __name__ == "__main__":
    v1 = Vector(p1=Point(x=3, y=5), p2=Point(x=7, y=8))
    print(v1)
    v2 = Vector(Point(x=9, y=5), Point(x=9, y=8))
    print(v2)
