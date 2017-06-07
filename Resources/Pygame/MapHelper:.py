class MapHelper:
    def __init__(self):
        self.minX = 1000
        self.minY = 1000
        self.maxX = 0
        self.maxY = 0

    def displace(self,lat,lng,theta, distance,unit="miles"):
        """
        Displace a LatLng theta degrees clockwise and some feet in that direction.
        Notes:
            http://www.movable-type.co.uk/scripts/latlong.html
            0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
        Args:
            theta:    A number in degrees where:
                      0   = North
                      90  = East
                      180 = South
                      270 = West
            distance: A number in specified unit.
            unit:     enum("miles","kilometers")
        Returns:
            A new LatLng.
        """
        theta = np.float32(theta)
        radiusInMiles = 3959
        radiusInKilometers = 6371

        if unit == "miles":
            radius = radiusInMiles
        else:
            radius = radiusInKilometers

        delta = np.divide(np.float32(distance), np.float32(radius))

        theta = deg2rad(theta)
        lat1 = deg2rad(lat)
        lng1 = deg2rad(lng)

        lat2 = np.arcsin( np.sin(lat1) * np.cos(delta) +
                          np.cos(lat1) * np.sin(delta) * np.cos(theta) )

        lng2 = lng1 + np.arctan2( np.sin(theta) * np.sin(delta) * np.cos(lat1),
                                  np.cos(delta) - np.sin(lat1) * np.sin(lat2))

        lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

        return [self.rad2deg(lat2), self.rad2deg(lng2)]

    def deg2rad(self,theta):
            return np.divide(np.dot(theta, np.pi), np.float32(180.0))

    def rad2deg(self,theta):
            return np.divide(np.dot(theta, np.float32(180.0)), np.pi)

    def lat2canvas(self,lat):
        """
        Turn a latitude in the form [-90 , 90] to the form [0 , 180]
        """
        return float(lat) % 180

    def lon2canvas(self,lon):
        """
        Turn a longitude in the form [-180 , 180] to the form [0 , 360]
        """
        return float(lon) % 360

    def canvas2lat(self,lat):
        """
        Turn a latitutude in the form [0 , 180] to the form [-90 , 90]
        """
        return ((float(lat)+90) % 180) - 90

    def canvas2lon(self,lon):
        """
        Turn a longitude in the form [0 , 360] to the form [-180 , 180]
        """
        return ((float(lon)+180) % 360) - 180


    def poly2canvas(self,poly):
        newPoly = []
        for p in poly:
            x,y = p
            y = y * -1
            x = self.lon2canvas(x)
            y = self.lat2canvas(y)

            if x > self.maxX:
                self.maxX = x
            if x < self.minX:
                self.minX = x
            if y > self.maxY:
                self.maxY = y
            if y < self.minY:
                self.minY = y
            newPoly.append((x,y))
        return newPoly

    def getExtremes(self):
        return [self.minX,self.minY,self.maxX,self.maxY]

    # Determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs. This function
    # returns True or False.  The algorithm is called
    # the "Ray Casting Method".
    def point_in_poly(self,x,y,poly):

        x = self.lon2canvas(x)
        y = self.lat2canvas(y)
        poly = self.poly2canvas(poly)
        n = len(poly)
        inside = False

        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside


def shiftPoints(self,points):
    shiftedPoints = []
    for p in points:
        x,y = p
        x = x-self.minX
        y = y-self.minY
        shiftedPoints.append([x,y])
    return shiftedPoints

def projectPoint(self,points):
    projectedPoints = []
    for p in points:
        x,y = p
        x = (x / self.maxX) * self.width
        y = (y / self.maxY) * self.height
        projectedPoints.append([x,y])
    return projectedPoints

class BoundingBox(object):
    def __init__(self, *args, **kwargs):
        self.lat_min = None
        self.lon_min = None
        self.lat_max = None
        self.lon_max = None
