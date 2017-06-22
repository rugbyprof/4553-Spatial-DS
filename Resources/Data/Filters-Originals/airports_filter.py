import json
import sys
import collections

f = open('/code/repos/4553-Spatial-DS/Resources/Data/WorldData/airports.json','r')

data = f.read()

data = json.loads(data)

geo_json = collections.OrderedDict()

geo_json["type"] = "FeatureCollection"
    

feature_list = []

for k,dict in data.items():
    properties = {}
    feature = collections.OrderedDict()
    for kk,ap in dict.items():
        properties[kk] = ap
    lat = properties['lat']
    lon = properties['lon']
    del properties['lat']
    del properties['lon']
    feature["type"] = "Feature"
    feature["properties"] = properties
    feature["geometry"] = {"type":"Point","coordinates": [lon, lat]}
    feature_list.append(feature)

geo_json["features"] = feature_list

f = open("/code/repos/4553-Spatial-DS/Resources/Data/WorldData/airports_geo_json.geojson","w")
f.write(json.dumps(geo_json, sort_keys=False,indent=2, separators=(',', ': ')))


# {
#     "type": "Feature",
#     "properties": {
#         "city": "Latacunga",
#         "country": "EC",
#         "elevation": 9205,
#         "iata": "LTX",
#         "icao": "SELT",
#         "lat": -0.906832993,
#         "lon": -78.6157989502,
#         "name": "Cotopaxi International Airport",
#         "tz": "America/Guayaquil"
#     },
#     "geometry": {
#         "type": "Point",
#         "coordinates": [-78.6157989502, -0.906832993]
#     }
# }