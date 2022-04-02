from point import Point
import math
import random
from vector import Vector

dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


class Ball(Point):
    """
    Ball inherits from Point.

    @method: destination       -- private method to give the bearing going from p1 -> p2
    @method: move              -- length in this context
    @method: xInBounds         -- Helper class to check ... I'll let you guess
    @method: yInBounds         -- Same as previous just vertically :)

    This class is used to move a ball (circle) in a better manner than simply adding or
    subtracting values to the x,y coordinates. Below is a walkthrough.

    Given a point: p1

    1) Create a random point somewhere else on the screen / world / board:
            distance = 100
            degrees = math.radians(random.randint(0,360))
            p2 = destination(distance,degrees)

    2) Now I can calculate a vector between P1 and P2 at a given velocity (scalar value
        to adjust speed)

            velocity = random.randint(1,MaxSpeed) # 1-15 or 20
            vectorOps = VectorOps(p1,p2,velocity)

    3) Finally I have a "step" that as applied to `p1` will move it toward `p2` at the given step.

            p1.x += vector.dx
            p1.y += vector.dy
    """

    def __init__(self, *args, **kwargs):
        Point.__init__(self, *args, **kwargs)

        self.center = kwargs.get("center", None)
        self.velocity = kwargs.get("velocity", 3)
        self.radius = kwargs.get("radius", 1)
        self.color = kwargs.get("color", (0, 0, 0))

        self.direction = kwargs.get("direction", random.choice(dirs))
        self.dx = kwargs.get("dx", 5)
        self.dy = kwargs.get("dy", 5)

        if not self.center:
            self.center = Point(x=self.x, y=self.y)
        # print(self.center)

        self.bearing = math.radians(random.randint(0, 360))
        self.dest = self.destination(100, self.bearing)
        self.vector = Vector(self.center, self.dest, velocity=self.velocity)

    def destination(self, distance, bearing):
        """Given a distance and a bearing find the point: P2 (where we would end up)."""
        cosa = math.sin(bearing)
        cosb = math.cos(bearing)
        return Point(self.x + (distance * cosa), self.y + (distance * cosb))

    def setRadius(self, r):
        self.radius = r

    def setDxDy(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def move(self, bounds=None):
        """Applies the "step" to current location and checks for out of bounds
        Params:
            bounds ()
        Returns:
        """
        # print(self)
        x = self.x
        y = self.y

        # Move temporarily
        x += self.vector.dx
        y += self.vector.dy

        # Check if in bounds
        # If it's not, then change direction
        if not self._xInBounds(bounds, x):
            self.vector.dx *= -1
            self._change_bearing(math.pi)
        if not self._yInBounds(bounds, y):
            self.vector.dy *= -1

        # Move any way because If we hit boundaries then we'll
        # go in the other direction.
        self.x += self.vector.dx
        self.y += self.vector.dy

        # Update center value of ball
        self.center.x = self.x
        self.center.y = self.y

    def _xInBounds(self, bounds, x):
        if x >= bounds.maxX or x <= bounds.minX:
            return False
        return True

    def _yInBounds(self, bounds, y):
        if y >= bounds.maxY or y <= bounds.minY:
            return False
        return True

    def _change_bearing(self, change):
        """Change Bearing
        Params:
            change (float)
        Returns:
            None
        """
        self.bearing = (self.bearing + change) % (2 * math.pi)

    def changeSpeed(self, new_velocity):
        self.dest = self.destination(100, self.bearing)
        self.velocity = new_velocity
        self.vector = Vector(self.center, self.dest, velocity=self.velocity)

    def _str__(self):
        s = f"[\n"
        s += f"  center: {self.center}\n"
        s += f"  radius: {self.radius}\n"
        s += f"  vector: {self.vector}\n"
        s += f"  velocity: {self.velocity,}\n"
        s += f"  color: {self.color}\n"
        s += f"  dxdy: {self.dx},{self.dy}\n"
        s += "]"
        return s

    def __repr__(self):
        s = self.__class__.__name__
        s += f"[\n"
        s += f"  center: {self.center}\n"
        s += f"  radius: {self.radius}\n"
        s += f"  vector: {self.vector}\n"
        s += f"  velocity: {self.velocity,}\n"
        s += f"  color: {self.color}\n"
        s += f"  dxdy: {self.dx},{self.dy}\n"
        s += "]"
        return s

    def setColor(self, color):
        self.color = color

    def setCardinalDirection(self, direction):
        assert direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        self.direction = direction

    def updateCardinalDirection(self):
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


if __name__ == "__main__":
    b1 = Ball(x=44, y=55)
    print(b1)
    b2 = Ball(4, 5, data={"key": "value"}, velocity=99, radius=900)
    print(b2)
