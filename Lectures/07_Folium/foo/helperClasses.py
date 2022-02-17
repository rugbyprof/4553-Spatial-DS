import json
import geopandas
from shapely.geometry import box, Polygon, LineString, Point
import sys
import os





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
    pass
