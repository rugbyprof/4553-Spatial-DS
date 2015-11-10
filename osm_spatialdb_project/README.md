### Osm Spatial Data Project

#### Files / Folders:

- **shape_files**: Folder containing all the shape files.
- **pantograph**: Local install of pantograph that's been altered for our purposes.
- **leaflet_example.html**: Plain html example using leaflet to show a map created by mapbox
- **main.py**: main driver for this project.

#### Pantograph

Pantograph contains 3 main files that were altered:

- handlers.py
- js/pantograph.js
- templates/index.html

#### handlers.py

This file handles the communication between `main.py` and `pantograph.js`. Anything we need to do from a javascript standpoint gets started in the `handlers.py` file.     


#### pantograph.js

This file contains the javascript class that gets loaded into the actual web page that gets run in the browser. The `handlers.py` file passes **messages** to this file according to instructions from the `main.py` file.

#### index.html

This is simply a webpage that I altered to include `mapbox.js` which allows us to display map data to place our routing on. The drawing canvas that pantograph draws on is simply superimposed over the map layer provided by mapbox. Getting things to line up will be interesting.


#### Comments:

The additional code I added is commented, so you should be able to make sense out of it.


###Note:

This is NOT a good solution! Routing, drawing layers on maps, etc. can all be done so easily using existing libraries, but I wanted to keep the level of implementation low enough to make you responsible for more than passing a couple of points to leaflet and letting it draw the shortest route on the map.

Also, pantograph / python is familiar to us and the learning curve shouldn't be too steep.

#### Libraries:

- networkx
- nx_spatial
- haversine
- pyshp


#### Packages

- PostGis
- QGIS
- GDAL Complete

#### Sites

- http://geojson.io/#map=15/26.1220/-98.1947
