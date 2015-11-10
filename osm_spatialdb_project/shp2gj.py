import shapefile
# read the shapefile
reader = shapefile.Reader("./shape_files/tl_2013_48_prisecroads/tl_2013_48_prisecroads.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
   atr = dict(zip(field_names, sr.record))
   geom = sr.shape.__geo_interface__
   buffer.append(dict(type="Feature",geometry=geom, properties=atr))

# write the GeoJSON file
from json import dumps
geojson = open("geojson_files/tl_2013_48_prisecroads.json", "w")
geojson.write(dumps({"type": "FeatureCollection","features": buffer}, indent=2) + "\n")
geojson.close()
