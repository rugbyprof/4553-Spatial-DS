import json
from rich import print
from rdp import rdp
import glob
import os


def Bbox(poly):
    """ Returns a bounding box, given a polygon (list of points)
    """
    minx = miny = 99999
    maxx = maxy = -99999
    for point in poly:
        if point[0] < minx:
            minx = point[0]
        if point[1] < miny:
            miny = point[1]
        if point[0] > maxx:
            maxx = point[0]
        if point[1] > maxy:
            maxy = point[1]
    return (minx, miny, maxx, maxy)


def boxInBox(major, minor):
    """ Checks if minor box is completely within major box.
    """
    return (minor[0] >= major[0] and minor[1] >= major[1]
            and minor[2] <= major[2] and minor[3] <= major[3])


def loadFeatures(path):
    """ Opens path and loads all geojson files
    """
    files = glob.glob(os.path.join(path,"*.geojson"))
    features = []

    for file in files:
        # open local geojson file
        with open(file) as f:
            temp = json.load(f)

            features.extend(temp['features'])

    return features


if __name__ == '__main__':

    countries = loadFeatures()
    print(f"Countries: {len(countries)}")

    # I made this box using geojson.io
    extremes = [[-122.87109375, -62.91523303947613],
                [-29.53125, -62.91523303947613],
                [-29.53125, 35.17380831799959],
                [-122.87109375, 35.17380831799959],
                [-122.87109375, -62.91523303947613]]

    majorBbox = Bbox(extremes)
    print(majorBbox)

    results = []

    for country in countries:
        countryBbox = country['properties']['bbox']
        if boxInBox(majorBbox, countryBbox):
            results.append(country)

    print(len(results))
    for country in results:
        print(country['properties']['name'])
