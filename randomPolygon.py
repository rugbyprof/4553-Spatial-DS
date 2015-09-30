import math
import random
import numpy as np

# Add ShapeModules (which holds Point,Rect,Polygon) folder to the path
# so we can use those shapes.
import sys
sys.path.append("./ShapeModules")

from Polygon import Polygon


class RandPolygon(object):
    def __init__(self,minDist=100,maxDist=1000,minPoints=3,maxPoints=1000,startY=33.230073,startX=-97.143826):
        self.minDist = minDist
        self.maxDist = maxDist
        self.minPoints = minPoints
        self.maxPoints = maxPoints
        self.randPoints = random.randrange(self.minPoints,self.maxPoints)
        self.startX = startX
        self.startY = startY

        self.currIteration = 0.0
        self.maxIteration = self.maxPoints

        self.polygon = Polygon()
        self.points = []

        self.generatePolygon()

    def destination(self,x,y,angle, distance):
        """
        Displace a LatLng angle degrees counterclockwise and some
        meters in that direction.
        Notes:
            http://www.movable-type.co.uk/scripts/latlong.html
            0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
        Args:
            angle:    A number in degrees.
            distance: A number in meters.
        Returns:
            A new LatLng.
        """
        angle = np.float32(angle)

        delta = np.divide(np.float32(distance), np.float32(3959))

        angle = self.deg2rad(angle)
        y1 = self.deg2rad(y)
        x1 = self.deg2rad(x)

        y2 = np.arcsin( np.sin(y1) * np.cos(delta) +
                          np.cos(y1) * np.sin(delta) * np.cos(angle) )

        x2 = x1 + np.arctan2( np.sin(angle) * np.sin(delta) * np.cos(y1),
                                  np.cos(delta) - np.sin(y1) * np.sin(y2))

        x2 = (x2 + 3 * np.pi) % (2 * np.pi) - np.pi

        return [self.rad2deg(x2),self.rad2deg(y2)]

    def deg2rad(self,angle):
            return np.divide(np.dot(angle, np.pi), np.float32(180.0))

    def rad2deg(self,angle):
            return np.divide(np.dot(angle, np.float32(180.0)), np.pi)

    def generatePolygon(self):
        pts = []
        n = self.randPoints
        for i in range(n):
            angle = self.randAngle(i,n,"Degrees")
            distance = random.randrange(self.minDist,self.maxDist)
            #print angle,distance
            xy = self.destination(self.startX,self.startY,self.rad2deg(angle),distance)
            pts.append((xy[0],xy[1]))
            #print xy[1],",",xy[0],":",self.getPointAngle(xy[0],xy[1])
        self.polygon.set_points(pts,(self.startX,self.startY))
        self.polygon.orderPoints()
        pts = self.polygon.get_points()
        for p in pts:
            print p[1],",",p[0],":"


    def randDistance(self):
        random.randrange(self.minDist,self.maxDist)

    """
    @private
    @method - randAngle: Generates a random angle between the ith and ith + 1 iteration.
                         Meaning that if this function was called 4 times, it would successively
                         return angles: 0-90,90-180,180-270,270-360
    @param {int} i      : Current iteration count (or starting angle)
    @param {int} n      : Max iterations (or ending angle)
    @param {string}     : Radians or Degrees
    @returns list[]: list of items in node
    """
    def randAngle(self,i,n,Units="Radians"):
        i = float(i)
        n = float(n)
        value = (2.0 * math.pi) * random.uniform((i)/n , (i+1)/n)
        if Units == "Radians":
            return value
        else:
            return math.degrees(value)


if __name__ == '__main__':

    lat = random.randint(31,47)
    lon = random.randint(75,121) * -1

    rp = RandPolygon(20,150,25,150,lat,lon)
