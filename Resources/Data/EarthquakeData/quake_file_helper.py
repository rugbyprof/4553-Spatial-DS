import glob
import os
import sys
import json

"""
This class helps read the NYC crime data.
Usage:
    fh = FileHelper()

    data = fh.get_data([2017]) #pass year in as list, get data for that year
    data = fh.get_data([2015,2016,2017]) #pass years in as list, get data for those years
"""
class FileHelper(object):
    def __init__(self):
        self.files = glob.glob('./*.json')

    def get_data(self,years=[]):
        data = {}

        for file in self.files:
            fyear = file.split('-')
            fyear = fyear[1].split('.')
            fyear = int(fyear[0])
            if fyear in years:
                f = open(file,'r')
                json_data = json.loads(f.read())
                year_quakes = [] 
                for quake in json_data['features']:
                    keep = {}
                    keep['geometry'] = quake['geometry']
                    keep['mag'] = quake["properties"]["mag"]
                    keep['magType'] = quake["properties"]["magType"]
                    keep['time'] = quake["properties"]["time"]
                    keep['place'] = quake["properties"]["place"]
                    keep['types'] = quake["properties"]["types"]
                    keep['rms'] = quake["properties"]["rms"]
                    keep['sig'] = quake["properties"]["sig"]
                    year_quakes.append(keep)
                data[fyear] = year_quakes

        return data
    
    def _read_file(self,filename,key):
        data = []
        with open(filename) as f:
            for line in f:
                line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
                if key is not None:
                    if key.lower() in line.lower():
                        data.append(line.strip().split(','))
                else:
                    data.append(line.strip().split(','))
        return data

years = [x for x in range(2015,2018)]

if __name__=='__main__':
    fh = FileHelper()
    data = fh.get_data(years)
    f = open('quake-2015-2017-condensed.json','w')
    f.write(json.dumps(data, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()