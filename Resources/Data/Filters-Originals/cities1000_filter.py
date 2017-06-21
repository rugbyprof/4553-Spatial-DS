import json

f = open('/code/repos/4553-Spatial-DS/Resources/Data/WorldData/cities1000.txt','r')

data = f.read()

data = data.split("\n")

filtered = {}

for d in data:
    tmp = d.split("\t")
    if tmp[8] not in filtered:
        filtered[tmp[8]] = []
    filtered[tmp[8]].append({"city-name":tmp[2],"lat":tmp[4],"lon":tmp[5],"country-code":tmp[8],"time-zone":tmp[-2]})

f = open("cities.json","w")
f.write(json.dumps(filtered, sort_keys=True,indent=2, separators=(',', ': ')))