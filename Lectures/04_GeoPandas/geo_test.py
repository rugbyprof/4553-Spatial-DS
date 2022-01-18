import geopandas as gpd
from rich import print
import json

import os
os.chdir("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/05_GeoPandas/")

df = gpd.read_file('cities.geojson')
print(df)

# bounds = df.boundary

# print(bounds)

# b = bounds.to_json()

# with open("boundary.json","w") as f:
#     f.write(json.dumps(b))