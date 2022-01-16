## GeoJson

GeoJson is a "superset" of the Json data standard. It uses the Json structure to hold geographic data. More specifically points, lines, and polygons. 

With points we can represent addresses and locations. With line strings we can represent: streets, highways and boundaries. And of course with polygons we can represent countries, states, provinces and more. Any combination of the above can pretty much be used to represent any geographic entity. GeoJson isn't restricted to only map type data (for lack of a better term), it can be used to represent overlays or shapes on top of maps to represent random things like cell phone coverage areas,  available parking spots, or wild fire smoke visibility.


### Geometry primitives

<center><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/SFA_Point.svg/51px-SFA_Point.svg.png" width="75"></center> 

A point represents a single location and is a list containing an `x` and `y` coordinate or a `longitude` and `latitude`.

```json
{
    "type": "Point", 
    "coordinates": [30.0, 10.0]
}
```

-----


|**LineString** |
|:---:|
| <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/SFA_LineString.svg/51px-SFA_LineString.svg.png" width="75"> |

To represent a line, you’ll need at least two places to connect but you can have more. Notice the square brackets surrounding all the points. A linestring is basically a list of points. 

```json
{
    "type": "LineString", 
    "coordinates": [
        [30.0, 10.0], [10.0, 30.0], [40.0, 40.0]
    ]
}
```
-----

|**Polygon** |
|:---:|
| <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/SFA_Polygon.svg/51px-SFA_Polygon.svg.png" width="75">|

Polygons are where GeoJSON geometries become significantly more complex. They have area, so they have *insides* & *outsides*. Notice we go one level deeper with the square brackets. You could think of a simple polygon as a `list of linestrings`. Each linestring much start and end with the same point. So a polygon is just a linestring that is a closed loop. 

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
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/SFA_Polygon_with_hole.svg/51px-SFA_Polygon_with_hole.svg.png" width="75">

By adding another set of points to this polygon, we can define a "hole" if those points are inside the initial polygon. If the second set of points was not included in the same set of outer square brackets, but rather had its own, it would be simply a different polygon (see MultiPolygon below ).

```json
{
    "type": "Polygon", 
    "coordinates": [
        [[35.0, 10.0], [45.0, 45.0], [15.0, 40.0], [10.0, 20.0], [35.0, 10.0]], 
        [[20.0, 30.0], [35.0, 35.0], [30.0, 20.0], [20.0, 30.0]]
    ]
}
```

By giving a polygon insides and outsides 

-----

### MultiPoint

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/SFA_MultiPoint.svg/51px-SFA_MultiPoint.svg.png" width="75">

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

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/SFA_MultiLineString.svg/51px-SFA_MultiLineString.svg.png" width="75">

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

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/SFA_MultiPolygon.svg/51px-SFA_MultiPolygon.svg.png" width="75">

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

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/SFA_MultiPolygon_with_hole.svg/51px-SFA_MultiPolygon_with_hole.svg.png" width="75">

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

### GeometryCollection

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