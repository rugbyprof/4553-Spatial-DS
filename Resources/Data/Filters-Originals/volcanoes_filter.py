import json
import sys

f = open('/code/repos/4553-Spatial-DS/Resources/Data/Filters-Originals/volcanos.csv','r')

data = f.read()

data = data.split("\r")

filtered = []

#Name,Country,Type,Lat,Lon,Altitude
skip = True
for line in data:
    if skip:
        skip = False
        continue
    line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
    line = line.decode('utf-8') 
    line = line.split(',')
    line[-1] = line[-1].strip()
    filtered.append({"Name":line[0].strip(),"Country":line[1],"Type":line[2],"Lat":line[3],"Lon":line[4],"Altitude":line[5]})


f = open("world_volcanos.json","w")
f.write(json.dumps(filtered, sort_keys=True,indent=2, separators=(',', ': ')))