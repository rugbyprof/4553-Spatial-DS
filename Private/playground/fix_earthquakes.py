import pprint as pp
import os,sys
import json
import collections


f = open("/code/repos/4553-Spatial-DS/Private/playground/display_world_features/geojson/earthquakes_1960_2017.geojson","r")

data = f.read()

data = json.loads(data)

all_quakes = []

"""
mongoimport --db world_data --collection volcanos --type json --file world_volcanos.geojson --jsonArray
db.volcanos.find( { loc: { $geoWithin: { $centerSphere: [ [140.8, 39.76 ] , 50 / 3963.2 ] } } } )

        {
            "geometry": {
                "coordinates": [
                    -176.248,
                    -24.678,
                    30
                ],
                "type": "Point"
            },
            "mag": 7.2,
            "magType": "mw",
            "place": "south of the Fiji Islands",
            "rms": null,
            "sig": 798,
            "time": -287255233000,
            "types": ",origin,"
        }

"""


for k,quakes in data.items():
    for e in quakes:
        eq = collections.OrderedDict()
        eq['type'] = "Feature"
        eq['geometry'] = {"type":"Point"}
        eq['geometry']['coordinates'] = [e['geometry']['coordinates'][0],e['geometry']['coordinates'][1]]
        depth = e['geometry']['coordinates'][2]
        del e['geometry']
        eq['properties'] = e
        eq['properties']['depth'] = depth
        eq['properties']['year'] = k
        all_quakes.append(eq)
    


out = open("/code/repos/4553-Spatial-DS/Private/playground/display_world_features/geojson/earthquakes.geojson","w")

out.write(json.dumps(all_quakes, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()