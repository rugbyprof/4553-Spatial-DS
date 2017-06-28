import json
import collections
import pprint

pp = pprint.PrettyPrinter(indent=4)

f = open("/code/repos/4553-Spatial-DS/Resources/Data/Filters-Originals/open_airports.csv","r")

data = f.read().split("\n")

print(len(data))
keys = "ID,Name,City,Country,IATA,ICAO,Lat,Lon,Altitude,Timezone,DST,Tz,Type,source".split(",")

aplist = []


#{"ID": "133", "Name": "Sudbury Airport", "City": "Sudbury", 
# #"Country": "Canada", "IATA": "YSB", "ICAO": "CYSB", "Lat": "46.625", "Lon": "-80.79889678955078", 
# "Altitude": "1141", "Timezone": "-5", "DST": "A", "Tz": "America/Toronto", "Type": "airport", "source": "OurAirports"}

for ap in data:
    apl = ap.replace('"','')

    apl = apl.split(",")
    if not len(apl) == 14:
        continue

    apdict = collections.OrderedDict()
    apdict['type'] = 'Feature'
    apdict['properties'] = {}
    for i in range(len(keys)):

        lat = float(apl[6])
        lon = float(apl[7])

        if apl[i] == "\\N":
            apl[i] = ""

        apdict['properties'][keys[i]] = apl[i]

    del apdict['properties']['Lat']
    del apdict['properties']['Lon']
    del apdict['properties']['source']
    

    print(lat,lon)
    geo = {'type':'Point','coordinates':[lon,lat]}
    apdict['geometry'] = geo
    aplist.append(apdict)

o = open("/code/repos/4553-Spatial-DS/Resources/Data/Filters-Originals/open_airports.geojson","w")
o.write(json.dumps(aplist, sort_keys=False,indent=4, separators=(',', ': ')))
o.close()

 