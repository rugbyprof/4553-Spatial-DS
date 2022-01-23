from rich import print

### Used by Griffin to set base directory with editing config files cause vscode is dumb
import os
os.chdir("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data")
### 

with open("cities_latlon_w_pop_v2.csv") as f:
    data = f.readlines()

keys = data[0]
del data[0]

states = {}

for row in data:
    items = row.strip().split(",")
    if not items[1] in states:
        states[items[1]] = []
    states[items[1]].append(items[0])



for key,value in states.items():
    print(f"{key},{len(value)}")


print(len(states))
