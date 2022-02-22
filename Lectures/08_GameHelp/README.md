## Worldle - Coding ideas


## Calculating Distance Between Polygons

The firs thing we need to do is calculate the distance between two polygons. We know Geopandas does this, but does it do it to the specifications that we need it to? That should be your first "experiment".

#### Experiment

1. Pick two countries and load the in to a spatial index.
2. Calculate the distance. 
3. Check that it "makes sense'
4. Goto 1. 

When picking countries you should obviously use the different case we discussed in class, but add even more. Listed below are some suggestions, but make sure you mix and match them.

- Countries on different continents.
- Countries right next to each other.
- Countries near the poles.
- Countries on the equator (or same longitude).
- Countries on the same latitude. 

### Methods for Polygon Distance

### Method 1 - Brute Force

- Calculate distance between every point in `Poly1` and `Poly2`.
- Sort on results and choose closest

### Method2 - Bounding Box

- Generate a minimum bounding rectangle and calculate the shortest distance between each point in `BBox1` and `BBox2`

### Method3 - Centroid

- Find the "center" of each polygon and calculate the distance between `Center1` and `Center2`

### Helper Classes

- You definitely need some code to help facilitate the talking points above. 
- I've included some code, but you need to write your own so you understand it!