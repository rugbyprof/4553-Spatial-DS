## File Formats - Convert and Display City Data
#### Due: 02-01-2022 (Tuesday @ 9:30 a.m.)

### Overview

The basic idea behind this program is to use Python to read in one file and output another.  The format of the input file can be csv or json and ultimately needs converting to proper `geoJson` format. Your resulting data file should be saved as a gist on `geoJson.io`.  What are you outputting? The goal is to create a geoJson file that contains a fictitious route visiting the single most populated city in each state. Only the continental US and DC, but not Alaska or Hawaii. I have my results below, which means you can probably find my resulting output file somewhere. I would encourage all of you to do your own work and don't steal mine :) 

<a href="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/spatial_prog1_example.png"><img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/spatial_prog1_example.png" width="400"></a>

Obviously this route is somewhat crazy, unless we had a private plane, and even then there are more efficient routes we could choose. Notice that the route goes from the west most city to the east most city, following a path placing the cities in order from west to east.


### Requirements

#### Input Files

You must use one of the following input files since ordering the cities is part of the programming problem:
- [cities_latlon_w_pop_.csv](../../Resources/01_Data/cities_latlon_w_pop.csv)
- [cities_latlon_w_pop_.json](../../Resources/01_Data/cities_latlon_w_pop.json)

I recommend the `json` file, but some of you are stubborn and will want to start with the csv. 

The data included in the file is the top 1000 US cities (based on population). I am not sure how accurate the list is, so please don't come to class and raise a stink claiming that some of the numbers are off. Below are to snippets from each file type showing the data elements.

**CSV Example:**
```csv
state,city,latitude,longitude,population,growth
Florida,Panama City,30.1588129,-85.6602058,36877,0.1
```

**Json Example:**
```json
{
    "city": "Panama City",
    "growth": 0.1,
    "latitude": 30.1588129,
    "longitude": -85.6602058,
    "population": 36877,
    "state": "Florida"
},
```

Read in one of the above files and process it in order to create a proper geoJson file. Here are a few things to remember:

- Only evaluate those cities in the continental United States (no Hawaii or Alaska).
- Identify the largest city in each state.
- After the most populated cities are found (49 of them) order the cities from west to east.
- Turn each city into a `Point` that is placed into a features list in a geoJson file.
- Each city will have a randomly (or some other coloring scheme) colored marker that is numbered by its order from west to east.
- Create a `LineString` connecting each city and place that in your features list as well. 

### GeoJson Help

Here is an empty geoJson object that represents a FeatureCollection:
```json
{
  "type": "FeatureCollection",
  "features": [
  ]
}
```

One Python equivalent to create a dictionary: 

```python
FeatureCollection = {}
FeatureCollection["type"] = "FeatureCollection"
FeatureCollection["features"] = []
```

I could've done this as well, but the above example gives a little better idea on how to add items to a dictionary: 

```python
FeatureCollection = {
  "type": "FeatureCollection",
  "features": []
}
```

At a minimum a `Feature` needs an empty properties object and a geometry object. In this case a `Point`: 

```json
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Point",
        "coordinates": [
          -122.676482,
          45.523062
        ]
      }
    }
```
However to make your geoJson file look like the requirements expect it to, you need the following properties: 

```json
    {
      "type": "Feature",
      "properties": {
        "marker-color": "#E23C71",
        "marker-size": "medium",
        "marker-symbol": 1
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          -122.676482,
          45.523062
        ]
      }
    }
```

Any additional properties, don't effect the output, they just stay with the feature as information:

```json
{
    "type": "Feature",
    "properties": {
        "state": "Oregon",
        "city": "Portland",
        "growth": 15,
        "population": 609456,
        "rank": 29,
        "marker-color": "#E23C71",
        "marker-size": "medium",
        "marker-symbol": 1
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
            -122.676482,
            45.523062
        ]
    }
}
```

To add this feature to my `FeatureCollection` dictionary, I simply append it to the features list. Assuming the snippet above is called `item`:

```python
FeatureCollection["features"].append(item)
```

If you try and understand the geoJson format by looking at the entire file at once, you will go crazy. You need to remember that it is organized into logical chunks, each component (nearly) independent of the rest. If you concentrate on creating each feature by itself, IMHO you will be more successful. For example, let's turn the following city into a feature:

```python
city = {
    "city": "Arlington",
    "growth": 13.3,
    "latitude": 32.735687,
    "longitude": -97.108065,
    "population": 379577,
    "state": "Texas"
}



def cityToPointFeature(city):
    # create an empty feature dictionary
    feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [0.0,0.0]
        }
    }

    # loop over our city dictionary
    # adding items to correct place
    for key,val in city.items():
        if 'longitude' in key:
            # if longitude in key make it the first item in coordinates
            feature["geometry"]["coordinates"][0] = val
        elif 'latitude' in key:
            # likewise, make latitude the second item in coordinates
            feature["geometry"]["coordinates"][1] = val
        else:
            # everything else gets put into properties
            feature["properties"][key] = val

    return feature
```

This would print out: 

```python
    feature = {
        "type": "Feature",
        "properties": {
            "city": "Arlington",
            "growth": 13.3,
            "population": 379577,
            "state": "Texas"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-97.108065,32.735687]
        }
    }
```

Now all you need to add is color and icon info by putting the proper key:values in the properties object. Then push that feature onto your featureList. 

```python
FeatureCollection["features"].append(city)
```

### Helper Code From Class

- [helper.py](helper.py)


### Deliverables

- Create a folder called `P01` in your `Assignments` folder within your repo.
- Make sure you have a README.md in your folder as well describing your project as dictated [here](../../Resources/02-Readmees/README.md).
- Include your geoJson file in the folder.
- Also include a screen shot and a link to your gist that contains your geoJson file so it can be viewed on geojson.io
