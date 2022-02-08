from doctest import Example
import json

f = open("example.geoJson")
data = json.load(f)

points = []
for feature in data["features"]:
    if feature["geometry"]["type"] == "Point":
        print(f'Point({feature["geometry"]["coordinates"]})')

polygons = []
for feature in data["features"]:
    if feature["geometry"]["type"] == "Polygon":
        polygon = []
        for line in feature["geometry"]["coordinates"]:
            for point in line:
                polygon.append(f"({point})")
            polygons.append(polygon)


print(polygons)
