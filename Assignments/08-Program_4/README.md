Program 4 - MongoDB 
=========

### Due: Wed Jun 27nd by Classtime

![](https://d3vv6lp55qjaqc.cloudfront.net/items/3f2W3H0N2h3H11402t3a/1024x512_cropped.png) 

### Overview

- Install MongoDB on your personal computer
    - Tutorial for [Windows](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
    - Tutorial for [Mac](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
    - Tutorial for [Linix](https://docs.mongodb.com/manual/administration/install-on-linux/) 

- Brush up on your [GeoJson](https://tools.ietf.org/html/rfc7946)


- Peruse a [NoSql Tutorial](http://no.sqlzoo.net/wiki/Main_Page)
- Install [PyMongo](https://api.mongodb.com/python/current/installation.html)
- Peruse a [PyMongo Tutorial](https://api.mongodb.com/python/current/tutorial.html)

- Do [THIS](http://tugdualgrall.blogspot.com/2014/08/introduction-to-mongodb-geospatial.html) tutorial.

Use https://gist.github.com to create a viewable rendition of your geojson file.


Incidentally a good tutorial: http://newcoder.io/dataviz/part-0/ (not necessary for assignment)


### Requirements
- The WorldData folder contains information about:
    - airports
    - earthquakes
    - city_locations
    - volcanos
    - countries
    - states 

- Some of these files have appropriate GeoJson formatted versions (e.g. _airports_geo_json.geojson_). And some don't. 
- Your assignment, due Wednesday is to create 6 GeoJson formatted files using the data in WorldData.
- These 6 files will be loaded into mongo db for the next assignment. 

### Deliverables
- Create a folder called `program_4` in your assignments folder.
- Create a folder called `geo_json` in your `program_4` folder.
- Create a file(s) called `generate_xxxx_geojson.py` where `xxxx` is one of the 6 data file names above.
- Each `generate_xxxx_geojson.py` file will read in the appropriate data file and create a correctly formatted GeoJson equivalent. 
- Your GeoJson output will be written to the `geo_json` folder.
- ***IMPORTANT:*** 
    - Only upload the first 1000 "objects" (volcanos, earthquakes, airports,etc) to github. 
    - You may want to include some kind of flag in your code to specify what size your output should be. 
    - The full size output should be the one that is loaded into mongo.
