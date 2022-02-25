from inspect import isclass
import json
import geopandas
from numpy import isin
from shapely.geometry import box, Polygon, LineString, Point
import sys
import os
from rich import print

validLatitude = range(-90, 91)
validLongitude = range(-180, 181)

validGeometryTypes = [
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]


def isClockWise(coords):
    """
    Determines if the points in a Polygon are clockwise or counter-clockwise

    Params:
        coords (list) : list of points
    Formula:
        (x_2 - x_1)(y_2 + y_1)
    Example:
        point[0] = (5,0)   edge[0]: (6-5)(4+0) =   4
        point[1] = (6,4)   edge[1]: (4-6)(5+4) = -18
        point[2] = (4,5)   edge[2]: (1-4)(5+5) = -30
        point[3] = (1,5)   edge[3]: (1-1)(0+5) =   0
        point[4] = (1,0)   edge[4]: (5-1)(0+0) =   0
                                                ---
                                                -44  counter-clockwise
    positive  = clockwise
    negative  = counter clockwise
    """
    sum = 0
    for i in range(len(coords) - 1):
        x1 = coords[i][0]
        x2 = coords[i + 1][0]
        y1 = coords[i][1]
        y2 = coords[i + 1][1]
        sum += (x2 - x1) * (y2 + y1)

    return sum >= 0


def isCounterClockWise(coords):
    """ Calls `counterClockWise` and returns a logical NOT of that result
    Params:
        coords (list) : list of points
    Returns:
        (bool) : True => points are counter clockwise False => points are clockwise 
    """
    return not isClockWise(coords)


def isPoint(point):
    """ Checks to see if a point: [x,y] or [lon,lat] has
        1: two integer or floating point values
        2: that the latitude and longitude are within ranges (-90,90 and -180,180)
    Params:
        point (list) : x,y coords or lon,lat coords
    Returns:
        (bool) : true => it is a valid point
    """
    return (
        (len(point) == 2)
        and (int(point[0]) in validLongitude)
        and (int(point[1]) in validLatitude)
    )


def isLineString(coords):
    """ Checks to see if a lineString (list of points) is valid

    Params:
        coords (list) : list of x,y points or list of lon,lat points
    Returns:
        (bool) : true => it is a valid lineString
    """
    # 1: is it a list
    if not isinstance(coords, list):
        return False
    # 2: check each point for validity
    for p in coords:
        if not isPoint(p):
            return False
    # 3: Its valid if code makes it here
    return True


def isMultiPoint(coords):
    """ A multiPoint is the same as a lineString so we simply call that method
    """
    return isLineString(coords)


def isMultiLineString(coords):
    """ Checks to see if a multiLineString (list of lineStrings) is valid

    Params:
        coords (list) : list of lineStrings
    Returns:
        (bool) : true => it is a valid multiLineString
    """
    # 1: is it a list
    if not isinstance(coords, list):
        return False
    # 2: are each lines valid lineStrings
    for line in coords:
        if not isLineString(line):
            return False
    # 3: Its valid if code makes it here
    return True




def isLinearRing(coords):
    """A linear ring is as follows:
        - Has 4 or more points
        - The first and last points are exactly the same

    Args:
        coords (list): a list of points to check for is "linearRing"

    Returns:
        bool: True = it is a linear ring
    """
    if not isinstance(coords, list):
        return False
    if len(coords) < 4:
        return False
    if coords[0] != coords[-1]:
        return False
    return True


def isPolygon(coords):
    """Checks for valid polygon format meaning:
    - It is a list of linear rings (which are lists of points)
    - The outer ring should be counter-clock wise
    - The inner rings (if any) should be clock wise
    """
    # basic container must be a list
    if not isinstance(coords, list):
        return False
    # look at each "line" of points
    for i in range(len(coords)):
        if i == 0:
            # outer ring must be counter-clockwise
            if not isCounterClockWise(coords[i]):
                return False
        else:
            # inner ring must be clockwise
            if not isClockWise(coords[i]):
                return False
        # lastly each line must be a valid linearRing
        if not isLinearRing(coords[i]):
            return False
    return True


def isMultiPolygon(coords):
    # basic container must be a list
    if not isinstance(coords, list):
        return False
    for polygon in coords:
        if not isPolygon(polygon):
            return False

    return True


class Feature(object):
    """Represents a feature that would exist in a geojson feature list

    Args:
        kwargs (dict): all params
            type (string)   : Point, LineString, Polygon, MultiPolygon
            coords (list)   : list of coordinates
            properties(dict): dictionary of key values
    """

    def __init__(self, **kwargs):
        type = kwargs.get("type", "Point")
        coords = kwargs.get("coords", [])
        properties = kwargs.get("properties", {})

        self.feature = {
            "type": "Feature",
            "geometry": {"type": type, "coordinates": coords},
            "properties": properties,
        }

    def setGeometryType(self, type):
        """Point, LineString, Polygon, MultiPolygon

        Args:
            type (string): valid geojson type
        """
        if type in validGeometryTypes:
            self.feature["geometry"]["type"] = type
        else:
            raise ValueError(f"Your type in `setGeometryType({type})` is not valid!")

    @property
    def __geo_interface__(self):
        if self.type in validGeometryTypes:
            return self

    def addCoords(self, coords):
        self.feature["geometry"]["coordinates"] = coords

    def addProperty(self, **kwargs):
        properties = kwargs.get("properties", None)
        key = kwargs.get("key", None)
        val = kwargs.get("val", None)

        if properties and isinstance(properties, dict):
            for key, val in properties.items():
                self.feature["properties"][key] = val
        elif properties and not isinstance(properties, dict):
            print(
                f"Error: `properties` kwarg existed and was not a dictionary. It was {type(properties)}"
            )
            sys.exit()

        if key and val:
            self.feature["properties"][key] = val


class FeatureCollection(object):
    def __init__(self, **kwargs):
        features = kwargs.get("features", [])
        self.featureCollection = {"type": "FeatureCollection", "features": features}

    def addFeature(self, kwargs):
        # numeric index location to place feature
        index = kwargs.get("index", None)

        # the feature to add
        feature = kwargs.get("feature", None)

    def addFeatures(self, **kwargs):
        pass


class GeoJsonHelper:
    def __init__(self, **kwargs):
        self.fileName = file_name

    def getFeature(self, **kwargs):
        # numeric index into feature array
        index = kwargs.get("index", None)

        # key value pair to look for under properties
        key = kwargs.get("key", None)
        val = kwargs.get("val", None)

    def addFeature(self, **kwargs):
        # numeric index location to place feature
        index = kwargs.get("index", None)

        # the feature to add
        feature = kwargs.get("feature", None)


class CountryHelper:
    def __init__(self, file_name, bbox=None):
        self.countryNames = []
        self.polygons = {}
        self.data = []
        self.polyCount = 0

        self.fileName = file_name
        self.loadFile()
        self.loadCountryPolys()

    def loadCountryPolys(self, file_name=None):
        if not file_name is None:
            self.loadFile(file_name)

        self.polyCount = 0
        for country in self.data:
            name = country["properties"]["name"]
            self.countryNames.append(name)
            self.polygons[name] = []

            for poly in country["geometry"]["coordinates"]:
                if len(poly) == 1:
                    self.polygons[name].append(
                        {"id": self.polyCount, "coords": poly[0]}
                    )
                    self.polyCount += 1
                else:
                    for subpoly in poly:
                        self.polygons[name].append(
                            {"id": self.polyCount, "coords": subpoly}
                        )
                        self.polyCount += 1

    def loadFile(self, file_name=None):
        if not file_name:
            file_name = self.fileName
        else:
            self.fileName = file_name

        if not os.path.isfile(self.fileName):
            print(f"Error: File {self.fileName} doesn't seem to exist!!")
            sys.exit()

        with open(self.fileName) as f:
            self.data = json.load(f)

        if "features" in self.data:
            self.data = self.data["features"]

        elif not isinstance(self.data, list):
            print("Error? Is file correct format?")
            sys.exit()

    def getCountryNameIndex(self, name):
        """Finds the index (integer) of a country by name

        Args:
            name (string): name of a country

        Returns:
            mixed: Either integer index of a country or None

        Example:
            getCountryNameIndex("Poland")
            returns: 40
        """
        if name in self.countryNames:
            return self.countryNames.index(name)
        return None

    def getCountryNames(self):
        return self.countryNames

    def getRawPolygons(self, country=None):
        if not country:
            return self.polygons

        for c, p in self.polygons.items():
            if c == country:
                return p

    def getCountryByPolyId(self, id):
        for country, polys in self.polygons.items():
            for poly in polys:
                if poly["id"] == id:
                    return country

    def getCountriesBySpatialResult(self, spatResult):
        results = []
        ids = []

        for i in range(len(spatResult)):
            if spatResult[i] == True:
                ids.append(i)

        for country, polys in self.polygons.items():
            for poly in polys:
                if poly["id"] in ids:
                    results.append(poly["id"])

        return results

    def getGeoPolygons(self):
        results = []
        for _, polys in self.polygons.items():
            for poly in polys:
                # print(poly)
                # print("")
                results.append(Polygon(poly["coords"]))
        return results

    def buildGeoJson(self, names, outname="outname.json"):
        results = {"type": "FeatureCollection", "features": []}
        for name in names:
            for country in self.data:
                if country["properties"]["name"] == name:
                    results["features"].append(country)

        with open(outname, "w") as f:
            json.dump(results, f, indent=4)


class SpatialIndexHelper(CountryHelper):
    def __init__(self):
        self.spi = geopandas.GeoSeries()

    def pointInPolygon(self, point):
        result = self.spi.contains(Point(point[0], point[1]))
        return result

    def polygonTouches(self, polygon):
        result = self.spi.touches(Polygon(polygon))
        return result

    def polygonOverlaps(self, polygon):
        result = self.spi.overlaps(Polygon(polygon))
        return result

    def lineIntersects(self, line):
        result = self.spi.intersects(LineString(line))
        return result

    def withinPolygon(self, polygon):
        result = self.spi.within(Polygon(polygon))
        return result


if __name__ == "__main__":
    f = Feature()

    print(f.feature)

    f.setGeometryType("Point")

    coords = [
        [
            [88.41796875, 36.1733569352216],
            [91.58203125, 32.99023555965106],
            [95.2734375, 35.31736632923788],
            [94.74609375, 37.996162679728116],
            [88.41796875, 36.1733569352216],
        ]
    ]

    poly = [
        [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
        [[100.8, 0.8], [100.8, 0.2], [100.2, 0.2], [100.2, 0.8], [100.8, 0.8]],
    ]

    print(isPolygon(poly))
    print(isClockWise(poly[0]))
    print(isClockWise(poly[1]))
