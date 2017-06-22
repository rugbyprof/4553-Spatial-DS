Program 4 - MongoDB 
=========

### Due: Tue Jun 27nd by Classtime

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


```mongo
db.airports.ensureIndex( { "geometry.coordinates" : "2d" })
```

Good Tutorial: http://newcoder.io/dataviz/part-0/



