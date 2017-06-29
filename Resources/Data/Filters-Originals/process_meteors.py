import json
import collections
import pprint as pp

f = open("/code/repos/4553-Spatial-DS/Resources/Data/Filters-Originals/meteorite-landings.csv","r")
o = open("/code/repos/4553-Spatial-DS/Resources/Data/WorldData/meteorite-landings.geojson","w")

keys = list(f.readline().strip().split(','))

print(keys)

data = f.read().split('\n')

meteor_list = []
line = 1
for d in data:
    print(line)
    meteor = collections.OrderedDict()
    meteor['type'] = 'Feature'
    meteor['properties'] = {}
    meteor['geometry'] = {}
    d = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(d.split('"')))
    d = d.split(',')
    for i in range(len(keys)):
        d[i] = d[i].replace('"','')
        if i == len(keys)-1:
            d[i] = d[i].strip()
        meteor['properties'][keys[i]] = d[i]
        print(keys[i],d[i])
    lat = meteor['properties']['reclat']
    lon = meteor['properties']['reclong']
    if not lat or not lon:
        continue

    del meteor['properties']['reclat']
    del meteor['properties']['reclong']
    del meteor['properties']['GeoLocation']
    meteor['geometry']['type'] = 'Point'
    meteor['geometry']['coordinates'] = [float(lon),float(lat)]
    line += 1
    meteor_list.append(meteor)

o.write(json.dumps(meteor_list, sort_keys=False,indent=4, separators=(',', ': ')))
