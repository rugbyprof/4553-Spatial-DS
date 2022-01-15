 
#protocol : computer / path
#https://cs.msutexas.edu/~griffin/data/FoodData/resaurant_updated_coord.json
import os
import sys
import json
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 #6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
    
# json.loads  - turns a vali json string into an object
# json.dumps - turns a valid object into a string
# serialization 


def readFile(name):
  """returns a list of dictionaries
  """
  jdata = []
  if os.path.isfile(name):
    with open(name) as f:
      data = f.readlines()
      for row in data:
        jdata.append(json.loads(row))
  return jdata
      

def countCuisines(data):
  """Counts unique cuisines
     cousines{
       "american":45,
       "chinese":3000,
       "other":234
       ...
     }
  """
  cuisines = {}
  for row in data:

    if not row['cuisine'] in cuisines:
      cuisines[row['cuisine']] = 0

    cuisines[row['cuisine']] += 1

  return cuisines

    
def saveCuisines(ddict):
  with open("cuisines.json","w") as f:
    f.write(json.dumps(ddict,indent=4))

  return os.path.isfile("cuisines.json")


def findClosest(ddict,lon1,lat1):
  mind = 9999999;
  rest = None

  for row in ddict:
    loc = row["location"]

    if len(loc['coordinates']) > 1:
      lon2 = loc['coordinates'][0]
      lat2 = loc['coordinates'][1]
      d = haversine(lon1, lat1, lon2, lat2)
      if d < mind:
        mind = d
        rest = row
  
  return rest



if __name__=='__main__':
  name = "restaurants.json"

  # loads our data
  data = readFile(name)

  # # count different cuisines
  # cuisines = countCuisines(data)

  # print(cuisines)
  # print(len(cuisines))
  # saveCuisines(cuisines)

  closest = findClosest(data,-73.986863, 40.71882)

  print(closest)



