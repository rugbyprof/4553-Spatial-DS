## GeoJson

source: https://datatracker.ietf.org/doc/html/rfc7946

### Point

For type "Point", the "coordinates" member is a single position.

Point coordinates are in x, y order (easting, northing for projected coordinates, longitude, and latitude for geographic coordinates):
```json
{
    "type": "Point",
    "coordinates": [100.0, 0.0]
}
```

### MultiPoint or LineString

Coordinates of a `MultiPoint` are an array of 2 or more positions:
```json
{
    "type": "MultiPoint",
    "coordinates": [
        [100.0, 0.0],
        [101.0, 1.0]
    ]
}
```

### MultiLineString

For type `MultiLineString`, the "coordinates" member is an array of `LineString` coordinate arrays.

```json
{
    "type": "MultiLineString",
    "coordinates": [
        [
            [100.0, 0.0],
            [101.0, 1.0]
        ],
        [
            [102.0, 2.0],
            [103.0, 3.0]
        ]
    ]
}
```

#### LinearRing

To specify a constraint specific to Polygons, it is useful to introduce the concept of a `linear ring`:

- A `linear ring` is a closed `LineString` with four or more positions.

- ***The first and last positions are equivalent***, and they MUST contain identical values; their representation SHOULD also be identical.

- A `linear ring `is the boundary of a surface or the boundary of a hole in a surface.

- A `linear ring` MUST follow the right-hand rule with respect to the area it bounds, **i.e., exterior rings are counterclockwise, and holes are clockwise.**

Note: the [GJ2008] specification did not discuss `linear ring` winding order.  For backwards compatibility, parsers SHOULD NOT reject `Polygons` that do not follow the right-hand rule.

Though a `linear ring` is not explicitly represented as a GeoJSON geometry type, it leads to a canonical formulation of the `Polygon` geometry type definition. See below.


### Polygons 
- For type `Polygon`, the "coordinates" member MUST be an array of `linear ring` coordinate arrays.

- For `Polygons` with more than one of these rings, the first MUST be the exterior ring, and any others MUST be interior rings.  The exterior ring bounds the surface, and the interior rings (if present) bound holes within the surface.

Coordinates of a Polygon are an array of linear ring ([see Section 3.1.6](https://datatracker.ietf.org/doc/html/rfc7946)) coordinate arrays.  The first element in the array represents the exterior ring.  Any subsequent elements represent interior rings (or holes).

**No holes:**
```json
{
    "type": "Polygon",
    "coordinates": [
        [
            [100.0, 0.0],
            [101.0, 0.0],
            [101.0, 1.0],
            [100.0, 1.0],
            [100.0, 0.0]
        ]
    ]
}
```

**With holes:**
```json
{
    "type": "Polygon",
    "coordinates": [
        [
            [100.0, 0.0],
            [101.0, 0.0],
            [101.0, 1.0],
            [100.0, 1.0],
            [100.0, 0.0]
        ],
        [
            [100.8, 0.8],
            [100.8, 0.2],
            [100.2, 0.2],
            [100.2, 0.8],
            [100.8, 0.8]
        ]
    ]
}
```

### MultiPolygon

For type `MultiPolygon`, the "coordinates" member is an array of `Polygon` coordinate arrays.

```json
{
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [102.0, 2.0],
                [103.0, 2.0],
                [103.0, 3.0],
                [102.0, 3.0],
                [102.0, 2.0]
            ]
        ],
        [
            [
                [100.0, 0.0],
                [101.0, 0.0],
                [101.0, 1.0],
                [100.0, 1.0],
                [100.0, 0.0]
            ],
            [
                [100.2, 0.2],
                [100.2, 0.8],
                [100.8, 0.8],
                [100.8, 0.2],
                [100.2, 0.2]
            ]
        ]
    ]
}
```
