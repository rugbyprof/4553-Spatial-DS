import csv
import json


def feature(coords, properties):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coords,
        },
        "properties": properties,
    }


def inUS(coords):
    # minx miny maxx maxy
    minx = -124.733174
    miny = 24.514962
    maxx = -66.949895
    maxy = 49.384358
    return (
        coords[0] >= minx
        and coords[0] <= maxx
        and coords[1] >= miny
        and coords[1] <= maxy
    )


csvfile = open("BetterUFOData.csv", "r")
jsonfile = open("ufo_bad_data.geojson", "w")


fieldnames = ("city", "state", "shape", "duration", "date_time", "lon", "lat")
reader = csv.DictReader(csvfile, fieldnames)
next(reader)

ufoFeatures = []
for row in reader:
    # print(row)
    properties = row
    coords = [float(row["lon"]), float(row["lat"])]
    # if not inUS(coords):
    #     continue
    del properties["lat"]
    del properties["lon"]

    ufoFeatures.append(feature(coords, properties))
    # print(ufoFeatures[-1])


fc = {"type": "FeatureCollection", "features": ufoFeatures}
json.dump(fc, jsonfile, indent=2, sort_keys=False)
jsonfile.write("\n")

# print(fl)
