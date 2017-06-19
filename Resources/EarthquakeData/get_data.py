import requests
import json
import sys


def get_earth_quake_data(year,month=[1,12],minmag=None,maxmag=None,query=True):
    start_month = month[0]
    end_month = month[1]

    if not maxmag is None:
        maxmag = '&maxmagnitude='+str(maxmag)
    else:
        maxmag = ''

    if not minmag is None:
        minmag = '&minmagnitude='+str(minmag)
    else:
        minmag = '&minmagnitude='+str(1.0)

    if query:
        type = 'query'

    else:
        type = 'count'

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/'+type+'?format=geojson&starttime='+str(year)+'-'+str(start_month)+'-01&endtime='+str(year)+'-'+str(end_month)+'-01'+minmag+maxmag

    r = requests.get(url).json()

    if type == 'count':
        return r['count']
    else:
        return r

path = '/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/EarthquakeData'
years = [x for x in range(1960,2017)]
months = [x for x in range(0,12)]

years = [2017]

for y in years:
    print("Year:%s" % (y))
    r = get_earth_quake_data(y,[1,12],5,None,True)
    f = open('./quake-'+str(y)+'.json','w')
    f.write(json.dumps(r, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()
    # r = get_earth_quake_data(y,[7,12],5,None,False)
    # f = open('./quake-'+str(y)+'.json','w')
    # f.write(json.dumps(r, sort_keys=True,indent=4, separators=(',', ': ')))
    # f.close()

