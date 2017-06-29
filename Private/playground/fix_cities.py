import pprint as pp
import os,sys
import json
import collections


f = open("/code/repos/4553-Spatial-DS/Resources/Data/WorldData/world_cities_small_w_pop.json","r")

data = f.read()

data = json.loads(data)

all_cities = []

"""
mongoimport --db world_data --collection volcanos --type json --file world_volcanos.geojson --jsonArray
db.volcanos.find( { loc: { $geoWithin: { $centerSphere: [ [140.8, 39.76 ] , 50 / 3963.2 ] } } } )

   "city": "Harare",
    "country": "Zimbabwe",
    "iso2": "ZW",
    "iso3": "ZWE",
    "lat": "-17.81778969",
    "lng": "31.04470943",
    "pop": "1557406.5",
    "province": "Harare"

"""


for v in data:
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = v
    if not v['lat'] and not v['lon']:
        continue

    lat = float(v['lat'])
    lon = float(v['lng'])
    
    del gj['properties']['lat']
    del gj['properties']['lng']
    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    gj["geometry"]["coordinates"] = [
          lon,
          lat
        ]
    all_cities.append(gj)


out = open("/code/repos/4553-Spatial-DS/Resources/Data/WorldData/world_cities.geojson","w")

out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()