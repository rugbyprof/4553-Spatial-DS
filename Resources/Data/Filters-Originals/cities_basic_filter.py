import json

f = open('/code/repos/4553-Spatial-DS/Resources/Data/WorldData/simplemaps-worldcities-basic.csv','r')

data = f.read()

data = data.split("\n")

print(data)

filtered = []

#city,city_ascii,lat,lng,pop,country,iso2,iso3,province
skip = True
for line in data:
    if skip:
        skip = False
        continue
    line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
    line = line.split(',')
    del line[0]
    line[-1] = line[-1].strip()
    filtered.append({"city":line[0],"lat":line[1],"lng":line[2],"pop":line[3],"country":line[4],"iso2":line[5],"iso3":line[6],"province":line[7]})


f = open("world_cities_small_w_pop.json","w")
f.write(json.dumps(filtered, sort_keys=True,indent=2, separators=(',', ': ')))