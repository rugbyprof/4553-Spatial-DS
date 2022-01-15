from rich import print
import json
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles. km 6371 Determines return value units.
    return c * r

geoData = []
with open("get_beer.geojson") as  f:
    data = f.read()
    geoData = json.loads(data)

coords1 = geoData["features"][1]['geometry']['coordinates']

# coords2 = []
# for feature in geoData['features']:
#     if "name" in feature["properties"]:
#         if feature["properties"]["name"] == "beer route":
#             for lon,lat in feature['geometry']['coordinates']:
#                         coords2.append((lon,lat))

# print(coords1)
# print(coords2)

lon1 = coords1[0][0]
lat1 = coords1[0][1]
lon2 = coords1[len(coords1)-1][0]
lat2 = coords1[len(coords1)-1][1]
print(f"Haversine distance as the crow flies: {haversine(lon1, lat1, lon2, lat2)}")

total = 0.0
for i in range(1,len(coords1)):
    total += haversine(coords1[i-1][0], coords1[i-1][1], coords1[i][0], coords1[i][1])

print(f"Haversine distance follow each point: {total}")
