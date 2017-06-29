import pprint as pp
import os,sys
import json
import collections
import itertools as IT

def area_of_polygon(x, y):
    """Calculates the signed area of an arbitrary polygon given its verticies
    http://stackoverflow.com/a/4682656/190597 (Joe Kington)
    http://softsurfer.com/Archive/algorithm_0101/algorithm_0101.htm#2D%20Polygons
    """
    area = 0.0
    for i in xrange(-1, len(x) - 1):
        area += x[i] * (y[i + 1] - y[i - 1])
    return area / 2.0

def centroid_of_polygon(points):
    """
    http://stackoverflow.com/a/14115494/190597 (mgamba)
    """
    area = area_of_polygon(*zip(*points))
    result_x = 0
    result_y = 0
    N = len(points)
    points = IT.cycle(points)
    x1, y1 = next(points)
    for i in range(N):
        x0, y0 = x1, y1
        x1, y1 = next(points)
        cross = (x0 * y1) - (x1 * y0)
        result_x += (x0 + x1) * cross
        result_y += (y0 + y1) * cross
    result_x /= (area * 6.0)
    result_y /= (area * 6.0)
    return (result_x, result_y)


f = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/Data/WorldData/state_borders.json","r")

data = f.read()

data = json.loads(data)

all_volcanos = []

"""
mongoimport --db world_data --collection volcanos --type json --file world_volcanos.geojson --jsonArray
db.volcanos.find( { loc: { $geoWithin: { $centerSphere: [ [140.8, 39.76 ] , 50 / 3963.2 ] } } } )
"""


for v in data:
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = {"name" : v["name"] , "code" : v["code"]}
    gj["geometry"] = {}
    if len(v['borders']) == 1:
        gj["geometry"]["type"] = "Polygon"
    else:
        gj["geometry"]["type"] = "MultiPolygon"

    gj["geometry"]["coordinates"] = v['borders']
    all_volcanos.append(gj)

out = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/Data/WorldData/state_borders.geojson","w")

out.write(json.dumps(all_volcanos, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()