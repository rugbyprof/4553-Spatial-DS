import json

with open("us_nation_border.geojson") as f:
    data = json.load(f)

minx = -123.2620435
miny = 25.4687224
maxx = -70.2553259
maxy = 48.74908

for multiPolygon in data["features"]:
    for i in range(len(multiPolygon)):
        print(i)
    # for polygon in multipPolygon["geometry"]["coordinates"]:
    #     for linestring in polygon:
    #         print(len(linestring))
    #         print(linestring)
    #         # for point in linestring:
    #         #     print(point)
