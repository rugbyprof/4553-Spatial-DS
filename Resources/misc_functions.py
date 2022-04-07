import pyqtree
import csv
import math
from math import sin, cos, sqrt, atan2, radians, asin
import sys
import numpy as np

AVG_EARTH_RADIUS = 6371  # in km

# Interesting source of functions
# http://www.edwilliams.org/avform.htm


def haversine(point1, point2, miles=True):
    """Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance between the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
    # unpack latitude/longitude
    lng1 = point1[0]
    lat1 = point1[1]
    lng2 = point2[0]
    lat2 = point2[1]

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
    if miles:
        return h * 0.621371  # in miles
    else:
        return h  # in kilometers


def bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[1])
    lat2 = math.radians(pointB[1])

    diffLong = math.radians(pointB[0] - pointA[0])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (
        math.sin(lat1) * math.cos(lat2) * math.cos(diffLong)
    )

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def cardinal(d, basic=False):
    """
    note: this is highly approximate...
    """
    if not basic:
        dirs = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
        ]
    else:
        dirs = [
            "N",
            "N",
            "N",
            "E",
            "E",
            "E",
            "S",
            "S",
            "S",
            "S",
            "S",
            "W",
            "W",
            "W",
            "N",
            "N",
        ]

    ix = int((d + 11.25) / 22.5 - 0.02)

    return dirs[ix % 16]


def midPoint(lat1, lon1, lat2, lon2):
    """
    Calculate the midpoint between two coordinate points
    """

    # phi = 90 - latitude
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)

    # theta = longitude
    lon1 = deg2rad(lon1)
    lon2 = deg2rad(lon2)

    X1 = cos(lat1) * cos(lon1)
    Y1 = cos(lat1) * sin(lon1)
    Z1 = sin(lat1)

    X2 = cos(lat1) * cos(lon1)
    Y2 = cos(lat1) * sin(lon1)
    Z2 = sin(lat1)

    X = (X1 + X2) / 2
    Y = (Y1 + Y2) / 2
    Z = (Z1 + Z2) / 2

    Lon = atan2(Y, X)
    Hyp = sqrt(X * X + Y * Y)
    Lat = atan2(Z, Hyp)

    lat = Lat * 180 / math.pi
    lon = Lon * 180 / math.pi

    return [lat, lon]


# def haversine(lon1, lat1, lon2, lat2):
#     """
#     Calculate the great circle distance between two points
#     on the earth (specified in decimal degrees)
#     """
#     # convert decimal degrees to radians
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

#     # haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     r = 3959 # Radius of earth in miles. Use 6371  for kilometers
#     return c * r


def displace(lat, lng, theta, distance, kilometers=True):
    """
    Displace a LatLng theta degrees counterclockwise and some
    meters in that direction.
    Notes:
        http://www.movable-type.co.uk/scripts/latlong.html
        0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
    Args:
        theta:    A number in degrees.
        distance: A number in meters.
    Returns:
        A new LatLng.
    """
    theta = np.float32(theta)

    units = 6371
    if not kilometers:
        units = 3959

    delta = np.divide(np.float32(distance), np.float32(units))

    theta = deg2rad(theta)
    lat1 = deg2rad(lat)
    lng1 = deg2rad(lng)

    lat2 = np.arcsin(
        np.sin(lat1) * np.cos(delta) + np.cos(lat1) * np.sin(delta) * np.cos(theta)
    )

    lng2 = lng1 + np.arctan2(
        np.sin(theta) * np.sin(delta) * np.cos(lat1),
        np.cos(delta) - np.sin(lat1) * np.sin(lat2),
    )

    lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

    return [rad2deg(lat2), rad2deg(lng2)]


def deg2rad(theta):
    return np.divide(np.dot(theta, np.pi), np.float32(180.0))


def rad2deg(theta):
    return np.divide(np.dot(theta, np.float32(180.0)), np.pi)


"""
@public
@method get_bounding_box: Creates a bounding box around a single point that is "half_side_in_miles"
                          away in every cardinal direction.
@param {float}-lat      : latitude
@param {float}-lon      : longitude
@param distance         : distance in miles
@returns {object}       : bounding box
"""


def get_bounding_box(lat, lon, distance):
    assert distance > 0
    assert lat >= -180.0 and lat <= 180.0
    assert lon >= -180.0 and lon <= 180.0

    lat = math.radians(lat)
    lon = math.radians(lon)

    radius = 3959
    # Radius of the parallel at given latitude
    parallel_radius = radius * math.cos(lat)

    lat_min = lat - distance / radius
    lat_max = lat + distance / radius
    lon_min = lon - distance / parallel_radius
    lon_max = lon + distance / parallel_radius
    rad2deg = math.degrees

    box = BoundingBox()
    box.lat_min = rad2deg(lat_min)
    box.lon_min = rad2deg(lon_min)
    box.lat_max = rad2deg(lat_max)
    box.lon_max = rad2deg(lon_max)

    return box


class BoundingBox(object):
    def __init__(self, *args, **kwargs):
        self.lat_min = None
        self.lon_min = None
        self.lat_max = None
        self.lon_max = None


# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".
def point_in_poly(self, x, y, poly):

    x = self.lon2canvas(x)
    y = self.lat2canvas(y)
    poly = self.poly2canvas(poly)
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


if __name__ == "__main__":
    print(5180 * haversine((-124.000, 34.000), (-124.0020, 34.0020)))
