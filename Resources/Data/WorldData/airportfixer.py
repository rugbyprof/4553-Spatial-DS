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

data1 = []
with open("airports_gj.geojson") as f:
    data1 = f.read()
    data1 = json.loads(data1)




count = 0

print("======================")
data2 = []
with open("airports_combined.geojson") as f:
    data2 = f.read()
    data2 = json.loads(data2)

i = 0
for feature in data1['features']:
    lon1,lat1 = feature['geometry']['coordinates']
    minDist = 9999999
    j = 0
    for ap in data2:
        lon2,lat2 = ap['geometry']['coordinates']
        dist = haversine(lon1, lat1, lon2, lat2)
        if dist < 1.1:
            count+=1
        if dist < minDist:
            minDist = dist
            minI = i
            minJ = j
        j += 1
    i += 1
    # print("============")
    # print(minDist,data1['features'][minI],data2[minJ])
print(count)
print(len(data1['features']))
print(len(data2))
        


