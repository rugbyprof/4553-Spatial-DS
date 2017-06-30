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



def get_bounds(c,info):
    for i in info:
        if i['countryCode'] == c['properties']['ISO_A2']:
            return {'north':float(i["north"]),'south':float(i["south"]),'east':float(i["east"]),'west':float(i["west"])}

f1 = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Private/playground/countries.geojson","r")
f2 = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/Data/WorldData/country_info.json","r")


countries = json.loads(f1.read())
infos = json.loads(f2.read())

all_countries = []

for c in countries['features']:
    bounds = get_bounds(c,infos)
    c['properties']['bounds'] = bounds
    all_countries.append(c)



out = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Private/playground/display_world_features/geojson/countries_with_bounds.geojson","w")

out.write(json.dumps(all_countries, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()