## GeoJson

GeoJson is a "superset" of the Json data standard. It uses the Json structure to hold geographic data. More specifically points, lines, and polygons. 

With points we can represent addresses and locations. With line strings we can represent: streets, highways and boundaries. And of course with polygons we can represent countries, states, provinces and more. Any combination of the above can pretty much be used to represent any geographic entity. GeoJson isn't restricted to only map type data (for lack of a better term), it can be used to represent overlays or shapes on top of maps to represent random things like cell phone coverage areas,  available parking spots, or wild fire smoke visibility.


## Geometry primitives

### Point

A point represents a single location and is a list containing an `x` and `y` coordinate or a `longitude` and `latitude`.

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/SFA_Point.svg/51px-SFA_Point.svg.png" width="125"></p> 

```json
{
    "type": "Point", 
    "coordinates": [30.0, 10.0]
}
```

-----

### LineString

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/SFA_LineString.svg/51px-SFA_LineString.svg.png"  width="125"></p> 


To represent a line, you’ll need at least two places to connect but you can have more. Notice the square brackets surrounding all the points. A LineString is basically a list of points. 

```json
{
    "type": "LineString", 
    "coordinates": [
        [30.0, 10.0], [10.0, 30.0], [40.0, 40.0]
    ]
}
```
-----

### Polygon

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/SFA_Polygon.svg/51px-SFA_Polygon.svg.png" width="125"></p>

Polygons are where GeoJSON geometries become significantly more complex. At its simplest however, it's really just a LineString enclosed in an additional set of brackets like the first example below. Additionally, each LineString must start and end with the same point. So a simple polygon is just a LineString that is a closed loop. 

```json 
{
  "type": "Polygon",
  "coordinates": [
    [
      [[35.0, 10.0], [45.0, 45.0], [15.0, 40.0], [10.0, 20.0], [35.0, 10.0]]
    ]
  ]
}
```

Where things get more complex is when we want to define a polygon with holes in it, basically defining the *insides* & *outsides* of the polygon. By adding another set of points to the above polygon, we can define a "hole" as long as those points are inside the initial polygon. 

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/SFA_Polygon_with_hole.svg/51px-SFA_Polygon_with_hole.svg.png" width="125"></p>

```json
{
    "type": "Polygon", 
    "coordinates": [
        [[35.0, 10.0], [45.0, 45.0], [15.0, 40.0], [10.0, 20.0], [35.0, 10.0]], 
        [[20.0, 30.0], [35.0, 35.0], [30.0, 20.0], [20.0, 30.0]]
    ]
}
```

Each entry when defining a polygon is called a LinearRing, and is organized like so:

- Polygon
  - LinearRing (exterior)
    - Positions..
  - LinearRing (interior)
    - Positions...
  - LinearRing (interior)
    - Positions...

The first LinearRing defines the perimiter and the remaining LinearRings define holes.

-----

## MultiShapes

These are geometry types that give us the ability to define multiple like items and putting them in the same container basically. GeoJson uses a concept known as "features" (defined below) to pair spatial data (coordinates) with other information known as "properties" (name, color ,etc.). If we didn't have multi-shapes we would have to provide the additional property information for each spatial construct. For example the MultiPoint below couldn't have 4 points belonging to the same geometry, it would have to be 4 Points all having their own property information. This is explained better in the next section.

### MultiPoint

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/SFA_MultiPoint.svg/51px-SFA_MultiPoint.svg.png" width="125"></p>

```json
{
    "type": "MultiPoint", 
    "coordinates": [
        [10.0, 40.0], [40.0, 30.0], [20.0, 20.0], [30.0, 10.0]
    ]
}
```

-----

### MultiLineString

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/SFA_MultiLineString.svg/51px-SFA_MultiLineString.svg.png" width="125"></p>

```json
{
    "type": "MultiLineString", 
    "coordinates": [
        [[10.0, 10.0], [20.0, 20.0], [10.0, 40.0]], 
        [[40.0, 40.0], [30.0, 30.0], [40.0, 20.0], [30.0, 10.0]]
    ]
}
```

### MultiPolygon

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/SFA_MultiPolygon.svg/51px-SFA_MultiPolygon.svg.png" width="125"></p>

```json
{
    "type": "MultiPolygon", 
    "coordinates": [
        [
            [[30.0, 20.0], [45.0, 40.0], [10.0, 40.0], [30.0, 20.0]]
        ], 
        [
            [[15.0, 5.0], [40.0, 10.0], [10.0, 20.0], [5.0, 10.0], [15.0, 5.0]]
        ]
    ]
}
```

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/SFA_MultiPolygon_with_hole.svg/51px-SFA_MultiPolygon_with_hole.svg.png" width="125"></p>

```json
{
    "type": "MultiPolygon", 
    "coordinates": [
        [
            [[40.0, 40.0], [20.0, 45.0], [45.0, 30.0], [40.0, 40.0]]
        ], 
        [
            [[20.0, 35.0], [10.0, 30.0], [10.0, 10.0], [30.0, 5.0], [45.0, 20.0], [20.0, 35.0]], 
            [[30.0, 20.0], [20.0, 15.0], [20.0, 25.0], [30.0, 20.0]]
        ]
    ]
}
```

## Features 

As mentioned in the previous section, `features` are basically spatial data paired with additional property information describing the spatial data (name, color, icon, etc.). GeoJson uses features as the most common building block for geoJson files. Each Feature needs 1) a type, 2) a geometry, and of course 3) properties. 

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [20, 30]
  },
  "properties": {
    "name": "null island",
    "marker-color": "#FFFF00",
    "marker-size": "medium"
  }
}
```


### GeometryCollection

One additional **type** geoJson can use is a GeometryCollection. I don't see this very often, but we need to know it exists.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/SFA_GeometryCollection.svg/51px-SFA_GeometryCollection.svg.png" width="75">

```json
{
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "Point",
            "coordinates": [40.0, 10.0]
        },
        {
            "type": "LineString",
            "coordinates": [
                [10.0, 10.0], [20.0, 20.0], [10.0, 40.0]
            ]
        },
        {
            "type": "Polygon",
            "coordinates": [
                [[40.0, 40.0], [20.0, 45.0], [45.0, 30.0], [40.0, 40.0]]
            ]
        }
    ]
}
``

### FeatureCollection

This is the majority of what we will see dealing with geoJson files. A feature collection is simply a list of "features" each having their own Type, Geometry, and Properties. 

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [0, 0]
      },
      "properties": {
        "name": "null island"
      }
    }
  ]
}
```

Here is a link to an example on [geoJson.io](http://geojson.io/#id=gist:rugbyprof/b745984fe6a79d4e5310a520854b39a9&map=2/10.3/0.0)

Sources:

- https://en.wikipedia.org/wiki/GeoJSON
- https://macwright.com/2015/03/23/geojson-second-bite.html