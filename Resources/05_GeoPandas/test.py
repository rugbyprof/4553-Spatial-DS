import geopandas as gpd
from rich import print
import json

df = gpd.read_file('cities.geojson')
#print(df)

bounds = df.boundary

print(bounds)

b = bounds.to_json()

with open("boundary.json","w") as f:
    f.write(json.dumps(b))