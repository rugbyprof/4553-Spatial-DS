import geopandas
import requests
import json
from shapely.geometry import box, Polygon, LineString, Point
import sys


class CountryPolyHelper:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.data = json.load(f)

        self.countryNames = []
        self.polygons = {}

        p = 0
        c = 0
        for country in self.data:
            name = country["properties"]["name"]
            self.countryNames.append(name)
            self.polygons[name] = []

            for poly in country["geometry"]["coordinates"]:
                # print(f"{row['properties']['name']} len:{len(poly)}")
                if len(poly) == 1:
                    self.polygons[name].append({"id": p, "coords": poly[0]})
                    p += 1
                else:
                    for subpoly in poly:
                        self.polygons[name].append({"id": p, "coords": subpoly})
                        p += 1
            c += 1

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
        results = []

        for name in names:
            for country in self.data:
                if country["properties"]["name"] == name:
                    results.append(country)

        with open(outname, "w") as f:
            json.dump(results, f, indent=4)


def pointInPolygon(spatialIndex, point):
    result = spatialIndex.sindex.query(Point(point[0], point[1]))
    return result


def polygonTouches(spatialIndex, polygon):
    result = spatialIndex.touches(Polygon(polygon))
    return result


def polygonOverlaps(spatialIndex, polygon):
    result = spatialIndex.overlaps(Polygon(polygon))
    return result


def lineIntersects(spatialIndex, line):
    result = spatialIndex.intersects(LineString(line))
    return result


def withinPolygon(spatialIndex, polygon):
    result = spatialIndex.within(Polygon(polygon))
    return result


if __name__ == "__main__":
    # instance of my helper class that loads the european countries
    cph = CountryPolyHelper("Europe.json")

    # get the polygons to build the spatial index
    polygons = cph.getGeoPolygons()

    print(f"Number of polygons: {len(polygons)}")
    s = geopandas.GeoSeries(polygons)

    # print some tests out
    # print(cph.getRawPolygons("France"))
    # print(cph.getCountryByPolyId(40))

    ##########################################################################3
    print(
        "Point in Polygon ##########################################################################"
    )
    # some points that are in different countries
    poland = [21.665039062499996, 50.401515322782366]
    albania = [20.123, 40.123]
    france = [2.28515625, 46.76996843356982]
    unk = [9.184570312499998, 42.16340342422401]

    # find polygon that contains the point
    result = pointInPolygon(s, unk)
    print(result)

    # find the country name(s) that are associated with the resulting polygon(s)
    for id in result:
        print(cph.getCountryByPolyId(id))
    sys.exit()
    ##########################################################################
    print(
        "Polygon Touches ##########################################################################"
    )
    rawPoly = cph.getRawPolygons("Serbia")

    # find polygons that touch the other polygon
    result = polygonTouches(s, rawPoly[0]["coords"])
    print(result)
    result = cph.getCountriesBySpatialResult(result)
    print(result)
    names = []
    for id in result:
        names.append(cph.getCountryByPolyId(id))
        print(cph.getCountryByPolyId(id))

    result = polygonOverlaps(s, rawPoly[0]["coords"])
    print(result)
    result = cph.getCountriesBySpatialResult(result)
    print(result)

    for id in result:
        names.append(cph.getCountryByPolyId(id))
        print(cph.getCountryByPolyId(id))

    geo = cph.buildGeoJson(names, "polytouches.json")

    ##########################################################################
    print(
        "Line Intersects ##########################################################################"
    )

    line = [[-2.373046875, 42.70759350405294], [29.70703125, 42.70759350405294]]
    result = lineIntersects(s, line)
    print(result)
    result = cph.getCountriesBySpatialResult(result)
    print(result)
    names = []
    for id in result:
        print(cph.getCountryByPolyId(id))
        names.append(cph.getCountryByPolyId(id))

    geo = cph.buildGeoJson(names, "lineintersects.json")
    sys.exit()
    ##########################################################################
    print(
        "Within Polygon ##########################################################################"
    )

    polygon = [
        [-3.1640625, 53.54030739150022],
        [44.29687499999999, 53.54030739150022],
        [44.29687499999999, 72.39570570653261],
        [-3.1640625, 72.39570570653261],
        [-3.1640625, 53.54030739150022],
    ]

    result = withinPolygon(s, polygon)
    print(result)
    result = cph.getCountriesBySpatialResult(result)
    print(result)
    for id in result:
        print(cph.getCountryByPolyId(id))
