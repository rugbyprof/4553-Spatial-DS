import json
import sys
import collections
from math import radians, cos, sin, asin, sqrt
import pprint as pp

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 6371 for km
    return c * r


'''
{u'geometry': {u'coordinates': [5.06992006302, 36.7120018005],
               u'type': u'Point'},
 u'properties': {u'ap_iata': u'BJA',
                 u'ap_level': u'3',
                 u'ap_name': u'Abane Ramdane Airport',
                 u'continent': u'Africa',
                 u'country': u'Algeria',
                 u'lat': u'36.7120018005',
                 u'lng': u'5.06992006302',
                 u'place_id': u'ChIJmfR9xijN8hIRC5Y1GXOjzT8',
                 u'sub_continent': u'North Africa'},
 u'type': u'Feature'}
{u'geometry': {u'coordinates': [5.069920063, 36.7120018005],
               u'type': u'Point'},
 u'properties': {u'city': u'Bejaia',
                 u'country': u'DZ',
                 u'elevation': 20,
                 u'iata': u'BJA',
                 u'icao': u'DAAE',
                 u'name': u'Soummam Airport',
                 u'tz': u'Africa/Algiers'},
 u'type': u'Feature'}
 '''

def combine_airport_data(ap1,ap2):
    for k,v in ap2['properties'].items():
        if k == 'iata':
            continue
        if k == 'country':
            nk = 'country_code'
        elif k == 'name':
            if ap1['properties']['ap_name'] == ap2['properties']['name']:
                continue
            else:
                nk = 'ap_name_2'
        else:
            nk = k
        ap1['properties'][nk] = ap2['properties'][k]
    return ap1

def same_airport(ap1,ap2,d):
    return ap1['properties']['ap_iata'] == ap2['properties']['iata'] or d < 2

f1 = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/Data/WorldData/jair_airports.geojson","r")
data1 = f1.read()
data1 = json.loads(data1)

f2 = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/Data/WorldData/airports_geo_json.geojson","r")
data2 = f2.read()
data2 = json.loads(data2)

f3 = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/Data/WorldData/airports_combined.geojson","w")

count = 0
match = 0
new_ap_list = []


for ap1 in data1:
    code1 = ap1['properties']['ap_iata']
    coord= ap1['geometry']['coordinates']
    lon1 = coord[0]
    lat1 = coord[1]
    closest = 99999
    for ap2 in data2:
        code2 = ap2['properties']['iata']
        coord= ap2['geometry']['coordinates']
        lon2 = coord[0]
        lat2 = coord[1]


        d = haversine(lon1,lat1,lon2,lat2)
        if d < closest:
            closest = d
            rec1 = ap1
            rec2 = ap2

        if same_airport(rec1,rec2,closest):
            match += 1
            # print(ap1['properties']['ap_iata'] ,   ap2['properties']['iata'])
            # print(closest)
            new_ap_list.append(combine_airport_data(rec1,rec2))
            break

    count += 1
    if count % 100 == 0:
        print(count)

print(len(new_ap_list))
print(new_ap_list[0])

f3.write(json.dumps(new_ap_list, sort_keys=False,indent=4, separators=(',', ': ')))
    # #print(closest)
    # if closest > 2.0 and closest < 5.0:
    #     count += 1
    #     print(closest)
    #     pp.pprint(rec1)
    #     pp.pprint(rec2)






