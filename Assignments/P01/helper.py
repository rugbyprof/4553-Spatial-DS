import json
from rich import print
import random

def randColor():
  r = lambda: random.randint(0,255)
  return ('#%02X%02X%02X' % (r(),r(),r()))


def makePoint(city):
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":randColor(),
      "marker-symbol": 'A'
    },
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }

  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      feature['geometry']['coordinates'][0] = val
    else:
      feature['properties'][key] = val

  return feature
  

# Change path as appropriate
with open("Resources/01_Data/cities_latlon_w_pop.json") as f:
  data = json.load(f)

states = {}

for item in data:
  if not item["state"] in states:
    states[item["state"]] = []

  states[item["state"]].append(item)


for state in states:
  print(f"{state} = {len(states[state])}")

points = []

for stateInfo in data:
  points.append(makePoint(stateInfo))

# Change path as appropriate
with open("Assignments/P01/almost_geojson.json","w") as f:
  json.dump(points,f,indent=4)
  
  