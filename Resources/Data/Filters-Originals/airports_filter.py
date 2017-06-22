import json
import sys

f = open('/code/repos/4553-Spatial-DS/Resources/Data/WorldData/airports.json','r')

data = f.read()

data = json.loads(data)


feature_list = []

for k,dict in data.items():
    properties = {}
    geo = {}
    for kk,ap in dict.items():
        properties[kk] = ap
    lat = properties['lat']
    lon = properties['lon']
    del properties['lat']
    del properties['lon']
    geo["type"] = "Feature"
    geo["properties"] = properties
    geo["geometry"] = {"type":"Point","coordinates": [lon, lat]}
    feature_list.append(geo)


f = open("/code/repos/4553-Spatial-DS/Resources/Data/WorldData/airports_geo_json.json","w")
f.write(json.dumps(feature_list, sort_keys=True,indent=2, separators=(',', ': ')))


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