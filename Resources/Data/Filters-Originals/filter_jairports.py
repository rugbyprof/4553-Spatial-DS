import json
import sys
import collections

sys.path.append('/Library/Python/2.7/site-packages')
from unidecode import unidecode

f = open("/code/repos/4553-Spatial-DS/Resources/Data/Filters-Originals/jairports.txt","r")

data = f.read()
data = data.replace("\\r","")
data = data.replace("\\","")
data = data.replace('"','')
# data = data.replace('{','')
# data = data.replace('}','')
data = data.replace(']','')
data = data.replace('[','')
#

data = data.split('}, {')

codes = {}
aplist = []
levels = [0,0,0,0]
#replace = ['u00f':'', 'u00e':'', 'u015':'', 'u00c':'', 'u002':'', 'u014':'', 'u021':'', 'u011':'', 'u02b':'', 'u010':'', 'u016':'', 'u017':'', 'u00d':'']

for d in data:
    d = d.split(',')
    apdict = collections.OrderedDict()
    apdict['type'] = 'Feature'
    apdict['properties'] = {}
    apdict['geometry'] = {'type':'Point'}

    for f in d:
        k,v = f.split(':')
        k = k.strip()
        v = v.strip()
        

        if k == 'lat':
            lat = v
        if k == 'lng':
            lon = v
        if k =='ap_name' and 'u0' in v:
            s = v.index('u0')
            code = ''
            for i in range(s,s+5):
                code+= v[i]
            if not code in codes:
                codes[code] = 0
            codes[code] += 1
        
        if 'ap_level' in k:
            k = 'ap_level'
            levels[int(v)] += 1


        apdict['properties'][k] = v
    apdict['geometry']['coordinates'] = [float(lon),float(lat)]
    aplist.append(apdict)

# o = open("/code/repos/4553-Spatial-DS/Resources/Data/Filters-Originals/jair_airports.geojson","w")
# o.write(json.dumps(aplist, sort_keys=False,indent=4, separators=(',', ': ')))
# o.close()

print(codes)
print(levels)
print(len(aplist))
# for code in codes:
#     code = "0x"+code[1:]
#     #hex = int(code,16)
#     #code = float.fromhex(code)
#     #print(unidecode(code))
#     print(code.decode('ascii'))
