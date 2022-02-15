import json
from rich import print
import sys

# geoData = {"type": "FeatureCollection", "features": []}

# continents = [
#     "Asia",
#     "Europe",
#     "Africa",
#     "Oceania",
#     "North America",
#     "Antarctica",
#     "South America",
#     "unk",
# ]


# load up continents and countries
# data = []
# with open("country-by-continent.json") as f:
#     data = json.load(f)

# create lookup dictionary
# lookup = {}
# for country in data:
#     lookup[country["country"]] = country["continent"]


# create a country by continent container
continentsDict = {}
# for continent in continents:
#     continentsDict[continent] = []

# list for countries that aren't recognized from the continents
missing = []


with open("world_borders-1-10.json") as f:
    data = json.load(f)

    for line in data["features"]:
        # del line["_id"]
        # line["properties"]["country"] = line["properties"]["admin"]
        # del line["properties"]["admin"]

        # line["properties"]["code"] = line["properties"]["ISO_A3"]
        # del line["properties"]["ISO_A3"]

        minx, miny, maxx, maxy = line["bbox"]

        polygon = [[minx, maxy], [maxx, maxy], [maxx, miny], [minx, miny], [minx, maxy]]

        line["properties"]["bbox"] = line["bbox"]
        line["properties"]["bbox_poly"] = polygon
        del line["bbox"]

        if not line["properties"]["continent"] in continentsDict:
            continentsDict[line["properties"]["continent"]] = []

        continentsDict[line["properties"]["continent"]].append(line)
        # else:
        #     missing.append(line["properties"]["admin"])
        #     continentsDict["unk"].append(line)

        # geoData["features"].append(line)


# print(sorted(missing))


# with open("countries.geojson", "w") as f:
#     json.dump(geoData, f, indent=4)


# print(continentsDict)

with open("country_by_continent/continents.json", "w") as f:
    json.dump(continentsDict, f, indent=4)

for continent, countries in continentsDict.items():
    with open(f"country_by_continent/{continent}.json", "w") as f:
        f.write(json.dumps(countries, indent=4))
