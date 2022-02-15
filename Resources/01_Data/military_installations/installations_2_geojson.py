import geopandas
from shapely.geometry import box, Polygon, LineString, Point


milShapeFile = geopandas.read_file("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data/FY20_MIRTA/FY20_MIRTA_Points.shp")

milShapeFile.to_file("base_locations.geojson", driver="GeoJSON")

milShapeFile2 = geopandas.read_file("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data/FY20_MIRTA/FY20_MIRTA_Boundaries.shp")

milShapeFile2.to_file("base_boundaries.geojson", driver="GeoJSON")