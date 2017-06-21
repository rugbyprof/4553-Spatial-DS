import json
import sys

f = open('/code/repos/4553-Spatial-DS/Resources/Data/WorldData/country_codes.csv','r')

data = f.read()

data = data.split("\n")

filtered = []

#Country or Area Name,ISO,ALPHA-2,ALPHA-3,ISO-Numeric

for line in data:
    line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
    line = line.split(',')
    del line[0]
    line[-1] = line[-1].strip()
    line[0] = line[0].replace(':',',').decode("utf-8", "replace")
    print(line)
    filtered.append({"Name":line[0],"Iso2":line[1],"Iso3":line[2],"IsoNumeric":line[3]})


f = open("country_codes.json","w")
f.write(json.dumps(filtered, sort_keys=True,indent=2, separators=(',', ': ')))