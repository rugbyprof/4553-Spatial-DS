from rich import print
import json
from shapely.geometry import Polygon
from math import radians, cos, sin, asin, sqrt
from area import area

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

def reproject(latitude, longitude):
    """Returns the x & y coordinates in meters using a sinusoidal projection"""
    from math import pi, cos, radians
    earth_radius = 6371009 # in meters
    earth_radius = 3958.8
    lat_dist = pi * earth_radius / 180.0

    y = [lat * lat_dist for lat in latitude]
    x = [long * lat_dist * cos(radians(lat)) 
                for lat, long in zip(latitude, longitude)]
    return x, y

def polygonArea(x, y):
    """Calculates the area of an arbitrary polygon given its verticies"""
    area = 0.0
    for i in range(-1, len(x)-1):
        area += x[i] * (y[i+1] - y[i-1])
    return abs(area) / 2.0


def getBoundingBox(coords):
    minLat = float('inf')
    minLon = float('inf')
    maxLat = float('-inf')
    maxLon = float('-inf')

    for lon,lat in coords:
        if lon < minLon:
            minLon = lon
        if lon > maxLon:
            maxLon = lon
        if lat < minLat:
            minLat = lat
        if lat > maxLat:
            maxLat = lat

    return {"minLon":minLon,"minLat":minLat,"maxLon":maxLon,"maxLat":maxLat}




geoData = []
with open("msu_polygon.geojson") as  f:
    data = f.read()
    geoData = json.loads(data)

lons = []
lats = []
coords = []
area1 = 0
for feature in geoData['features']:
    if feature["properties"]["name"] == "msuBorder":
        area1 = area(feature['geometry'])
        for coordinates in feature['geometry']['coordinates']:
                for lon,lat in coordinates:
                    coords.append((lon,lat))
                    lons.append(lon)
                    lats.append(lat)

x,y = reproject(lats, lons)

print(f"local function area: {polygonArea(x, y)}")              # local function for area
print(f"shapely library area: {Polygon(list(zip(x, y))).area}")  # shapely library
print(f"area library area: {float(area1)*0.00000038610215855}")


bbox = getBoundingBox(coords)         # create a bounding box around MSU perimeter (polygon)
print("bounding box:")
print(bbox)

# print the height of bounding box in miles

print(f"Height of campus: {haversine(bbox['minLon'], bbox['minLat'], bbox['minLon'], bbox['maxLat'])}")

# print width of bounding box in miles
print(f"Width of campus: {haversine(bbox['minLon'], bbox['minLat'], bbox['maxLon'], bbox['minLat'])}")


