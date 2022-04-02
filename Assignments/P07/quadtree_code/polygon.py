import sys
import math
import random
from point import Point
from rectangle import Rectangle


class Polygon(object):
    def __init__(self, *args, **kwargs):
        """Initialize a polygon from list of points."""
        self.points = []
        self.mbr = None

        # get list of points passed in ...
        if len(args) == 1:
            pts = args[0]
        else:
            pts = kwargs.get("points", [])

        self.centroid = kwargs.get("centroid", None)

        if len(pts) > 0:
            self.setPoints(pts, self.centroid)

    def setPoints(self, pts, centroid=None):
        """Reset the poly coordinates."""
        if centroid:
            self.centroid = Point(centroid[0], centroid[1])
        else:
            self.centroid = None

        self.minX = pow(2, 30)
        self.minY = pow(2, 30)
        self.maxX = pow(2, 30) * -1
        self.maxY = pow(2, 30) * -1

        self.points = []

        for p in pts:
            x = p.x
            y = p.y

            if x < self.minX:
                self.minX = x
            if x > self.maxX:
                self.maxX = x
            if y < self.minY:
                self.minY = y
            if y > self.maxY:
                self.maxY = y

            self.points.append(Point(x, y))

        self.mbr = Rectangle(Point(self.minX, self.minY), Point(self.maxX, self.maxY))

    def getPoints(self):
        """Get a plain list of tuple points
        Params:
            None
        Returns:
            points (List[tuples])
        """
        generic = []
        for p in self.points:
            generic.append(p.asTuple())
        return generic

    def pointInsidePolygon(self, p):
        """Determine if a point is inside a given polygon or not.
           Assuming Polygon is a list of (x,y) pairs.
        Params:
            p (Point)
        Returns:
            bool : True = point in polygon
        """
        n = len(self.points)
        inside = False

        p1x, p1y = self.points[0].asTuple()
        for i in range(n + 1):
            p2x, p2y = self.points[i % n].asTuple()
            if p.y > min(p1y, p2y):
                if p.y <= max(p1y, p2y):
                    if p.x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (p.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or p.x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def orderPoints(self):
        """ """
        assert not self.centroid == None

        ptsDict = {}
        for p in self.points:
            ptsDict[self.angleWithRespect2Centroid(p.x, p.y)] = p
            # print self.angleWithRespect2Centroid(p.x,p.y)
        self.points = []
        for key in sorted(ptsDict):
            # print "%s: %s" % (key, ptsDict[key])
            self.points.append(ptsDict[key])

    def calcArea(self, x, y):
        """Calculates the signed area of an arbitrary polygon given its verticies
        http://stackoverflow.com/a/4682656/190597 (Joe Kington)
        http://softsurfer.com/Archive/algorithm_0101/algorithm_0101.htm#2D%20Polygons
        """
        area = 0.0
        for i in range(-1, len(x) - 1):
            area += x[i] * (y[i + 1] - y[i - 1])
        return area / 2.0

    def calcCentroid(self):
        """
        http://stackoverflow.com/a/14115494/190597 (mgamba)
        """
        area = self.calcArea(*zip(*points))
        points = self.points
        result_x = 0
        result_y = 0
        N = len(points)
        points = IT.cycle(points)
        x1, y1 = next(points)
        for i in range(N):
            x0, y0 = x1, y1
            x1, y1 = next(points)
            cross = (x0 * y1) - (x1 * y0)
            result_x += (x0 + x1) * cross
            result_y += (y0 + y1) * cross
        result_x /= area * 6.0
        result_y /= area * 6.0
        return (result_x, result_y)

    def angleWithRespect2Centroid(self, x, y):
        assert not self.centroid == None

        return math.atan2(y - self.centroid.y, x - self.centroid.x)

    def __str__(self):
        return "<Polygon \n Points: %s \n Mbr: %s \n Centroid: %s>" % (
            "".join(str(self.points)),
            str(self.mbr),
            str(self.centroid),
        )

    def __repr__(self):
        return "%s %s" % (self.__class__.__name__, "".join(str(self.points)))


if __name__ == "__main__":
    points = [Point(4, 5)]
    for i in range(10):
        points.append(Point(random.randint(1, 10), random.randint(1, 10)))
    points.append(points[-1])

    p = Polygon(points)
    print(p)
