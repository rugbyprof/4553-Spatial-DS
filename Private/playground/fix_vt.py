import json

f = open("/Users/griffin/Desktop/vt.json","r")

data = f.read()

data = json.loads(data)

data['geometry']['coordinates'][0] = list(reversed(data['geometry']['coordinates'][0]))

o = open("/Users/griffin/Desktop/vt_rev.json","w")
o.write(json.dumps(data, sort_keys=False,indent=4, separators=(',', ': ')))