## No Path Still - Rtree Nearest Neighbor with UFO's
#### Due: 02-22-2022 (Tuesday @ 9:30 a.m.)

### Overview

We discussed in class that the master plan is to find some kind of optimal route from the west coast to the east coast visiting every city. It has been problematic finding connected road networks available for download, and processable by us. We decided in class today to use NetworkX and create a fully connected graph between all the cities, without using roads, and simply connecting each city "as the crow flies" using straight lines. We were also going to use UFO sightings as a metric for which cities to visit. Basically visit cities with lots of UFO sightings before visiting cities that had fewer UFO sightings. 

Let's shift gears and take a half step back. I want to forgo networkX for now, and simply concentrate on loading up our GeoPandas GeoSeries (spatial index / Rtree) with all the cities and UFO sightings. Once we have all of these point locations loaded, we can determine which cities have the most UFO sightings in close proximity and worry about routing between them in the next installment of this assignment. 

### Necessary Files 

Example Code
- [spatIndex.ipynb](spatIndex.ipynb)  
- [boundingBox.py](boundingBox.py) 

Data
- [./data_files/cities.geojson](data_files/cities.geojson)
- [./data_files/ufo_data.csv](data_files/ufo_data.csv)

### Extra Files

- Much bigger list of cities: [cities.csv](data_files/cities.csv) 
- [Example geojson](data_files/example.geojson) file used in the spatIndex.ipynb file.
- Proof that OsmNX library hates me: [Osmnx](osmnxExample.ipynb)

### Requirements

- Load at least on of the data files into a geopandas geoseries spatial index. Most likely, the UFO data will work the best using the spatial-index. 
- Calculate the distance from each city to every other city and store those values in either a csv or json file for use at a later time. This does not need a geospatial index, just a little brute force and a distance function.
- Determine a metric or threshold to "assign" a UFO sighting to a particular city. Maybe average the distance to the 100 closest UFO's as a start. 
- Your files should be in json format.


> Note: We could use a clustering algorithm to determine the spatial proximity to each of our 49 cities, but I think we could use a bounding box for now to keep it simple and keep it within the realm of our example code. I'm not sure what size the box should be, but it also brings another spatial structure to mind: [voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram), which we could use to create polygons around each city (but we won't), but could be used to query UFO sightings with each "cell".  

```python
def haversineDistance(lon1, lat1, lon2, lat2, units="miles"):
    """Calculate the great circle distance in kilometers between two points on the earth (start and end) where each point
        is specified in decimal degrees.
    Params:
        lon1  (float)  : decimel degrees longitude of start (x value)
        lat1  (float)  : decimel degrees latitude of start (y value)
        lon2  (float)  : decimel degrees longitude of end (x value)
        lat3  (float)  : decimel degrees latitude of end (y value)
        units (string) : miles or km depending on what you want the answer to be in
    Returns:
        distance (float) : distance in whichever units chosen
    """
    radius = {"km": 6371, "miles": 3956}

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = radius[units]  # choose miles or km for results
    return c * r
```

### Deliverables

- Create a folder called `P02` in your assignments folder on your repo.
- Add your file holding all the distances from each city to one another.
- Add a file that contains the average distance to the 100 closest UFO's for each city.
- Your file can be in any format that you can read back into another program to be processed.
- Place a copy of your output file in P02 and a small write up in a README file explaining the choices you made. 
- Please refer to the [Readmees](../../Resources/02-Readmees/README.md) folder for help on creating a worthwhile readme.
