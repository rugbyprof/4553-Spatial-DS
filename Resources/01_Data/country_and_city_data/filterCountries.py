""" Grab countries based on bounding box.
"""
import json

with open("countries.geojson") as f:
    data = json.load(f)


print(len(data["features"]))


continents = []
with open("country-by-continent.json") as f:
    lookup = json.load(f)


for country in lookup:
    if not country["continent"] in continents:
        continents.append(country["continent"])


print(len(continents))
print(continents)
