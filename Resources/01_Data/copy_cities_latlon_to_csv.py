"""
This script will read in a json file containing city data and will convert it to csv
simply for the reason to show csv and json use with pandas.

Json file looks like the following: 
[
    {
        "city": "New York",
        "growth": 4.8,
        "latitude": 40.7127837,
        "longitude": -74.0059413,
        "population": 8405837,
        "rank": 1,
        "state": "New York"
    },
    ...
]
"""

import json
import csv

### Used by Griffin to set base directory with editing config files cause vscode is dumb
import os
os.chdir("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data")
### 

def json_to_csv():
    csvOutFile = open('cities_latlon_w_pop.csv', 'w')

    # open json file into dictionary
    with open("./cities_latlon_w_pop.json") as f:
        cityData = json.load(f)

    # create the csv writer object
    csv_writer = csv.writer(csvOutFile)

    # get headers for csv by looking at first object in list of objects 
    header = cityData[0].keys()

    # write them to our csv_writer
    csv_writer.writerow(header)

    for city in cityData:
        # Writing data of CSV file
        csv_writer.writerow(city.values())
    
    csvOutFile.close()

def json_to_csv_reorder_columns():
    old_header = ['city','growth','latitude','longitude','population','rank','state']
    new_header = ['rank','state','city','latitude','longitude','population','growth']

    csvOutFile = open('cities_latlon_w_pop_v2.csv', 'w')

    # open json file into dictionary
    with open("./cities_latlon_w_pop.json") as f:
        cityData = json.load(f)

    # create the csv writer object
    csv_writer = csv.writer(csvOutFile)

    # write the new header to our csv_writer
    csv_writer.writerow(new_header)

    for city in cityData:
        row = []
        for key in new_header:
            row.append(city[key])
        
        csv_writer.writerow(row)
    
    csvOutFile.close()

if __name__=='__main__':
    json_to_csv()
    json_to_csv_reorder_columns()
    