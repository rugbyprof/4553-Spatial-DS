Heat Map
========

NOT DONE!!!

## Overview

Generate a heat style map showing terrorist hotspots around the world. You have a couple of choices of how to get this done:
1. Grid method 
2. Count City method

### Grid Method

The grid method takes the geometry of each occurence and after converting the coordinates to xy values, it maps them into a 2d array (x val = row index and y val = column index). Every time a coordinate maps to a cell, simply increase the value of that cell by one, keeping a count. The number of occurences of each cell will be assigned a color value based on the function below, where the highest occuring value will get assigned the "hottest" color (red), and the least occuring values will get assigned the "coolest" color (blue).

How you display your grids on the map is up to you. You could represent each grid cell as a box or rectangle thereby coloring the area of the map that it represented. Or, you could use another shape or icon and change the color and or size based on its value. As long as your visual output makes it very apparent where the "hot spots" are.  

#### Pseudo Code for Grid
- <sup>Source: https://stackoverflow.com/questions/2343681/algorithm-for-heat-map</sup>



**Create Grid**
```
grid = [][]
for each (lon,lat) in list:
  x,y = adjusted(lon,lat)
  grid[x][y]++
end
```
<sub>This is PSEUDO code ... it does NOT run</sub>
>This would create your grid. Rows and columns would need to be figured out before hand
based on screen size, and number of data points (for visual effect). Remember, with more
cells a finer grained heat map is created. Less cells would create large blocks of 
color.

--------

If you want to create a grid using the lat lon values instead of adjusted x,y coordinates, it may be a good choice, especially if you know what granularity to choose. The table below tells us how precise a lat,lon coordinate is based on how many decimal places it contains. 

|places|precision|qualitative scale |N/S or E/W at equator|E/W at 23N/S|E/W at 45N/S|E/W at 67N/S|
|--------|--------|--------|--------|--------|--------|--------|
|0|1.0|country or large region|111.32 km|102.47 km|78.71 km|43.496 km|
|1|0.1|large city or district|11.132 km|10.247 km|7.871 km|4.3496 km|
|2|0.01|town or village|1.1132 km|1.0247 km|787.1 m|434.96 m|
|3|0.001|neighborhood, street|111.32 m|102.47 m|78.71 m|43.496 m|
|4|0.0001|house w/ property |11.132 m|10.247 m|7.871 m|4.3496 m|
|5|0.00001|individual trees|1.1132 m|1.0247 m|787.1 mm|434.96 mm|
|6|0.000001|individual humans|111.32 mm|102.47 mm|78.71 mm|43.496 mm|
|7|0.0000001|commercial surveying|11.132 mm|10.247 mm|7.871 mm|4.3496 mm|
|8|0.00000001|tectonic plate mapping|1.1132 mm|1.0247 mm|787.1 µm|434.96 µm|

<sup>source: https://en.wikipedia.org/wiki/Decimal_degrees </sup>

The `terrorism collection` contains the following precision where key = precision (decimal places) and value = count. So the majority of the collection (120000+) contain 6 decimals or more. 
>- {0: 50, 1: 2980, 2: 2918, 3: 1085, 4: 2781, 5: 15027, 6: 125325, 7: 1593, 8: 494}
>- {0: 188, 1: 3283, 2: 3271, 3: 663, 4: 4005, 5: 18176, 6: 120556, 7: 1573, 8: 513, 9: 25}

So how do we "bucket" lat/lons?
- Add 180 to lon's (gives a value from 0-360)
- Add 90 to lat's (gives a value from 0-90)
- Using each of those rounded values we could get a 2D grid of 360x90 
- If we multiply each value by 10 then round (or truncate) we could get a 2D grid of 3600x900 (way too much for us).
- If we multiply each value by 5 then round (or truncate) we could get a 2D grid of 1800x450.
- ***Why don't we stick to the adjusted x,y coords method!***

------

**Expand/Blur Colors**
```
P = N #number of passes
for 0 to P:
  for each row:
   for each col:
     if grid[row][col] > 0 then:
       increment_adjacent_cells(row, col)
     end
   end
  end
end
```
>There are other algorithms to "blur" a 2D array of pixels (gaussian most popular), 
but here is a method to let a strong (high heat) value bleed into neighboring cells.
This technique would work best with lots of cells. 
>
>- The idea is to pass over the grid ___`N`___ number of times. 
>- Each pass you increment "adjacent" cells. Where _Adjacent_ = 8 neighboring cells. 
>- Depending on the number of passes, your "hot" areas will expand accordingly.

#### Count Cities

After writing the previous section (Grid Method), I prefer that spatial solution using geometries over this method. Why? Because every object has a geometry, compared to this method of selecting and filtering on "city" which has 6000 entries labeled as "unknown". Having said that, I did create a json object with the following structure if anyone wants to use it to help with this problem:

```json
"country_1_name": {
        "city_1_name": {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    123.456,
                    -2.3456
                ]
            },
            "count": 7
        },
        "city_2_name": {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    34.5678,
                    23.4567
                ]
            },
            "count": 19
        },
        "etc":"..."
    }
    "country_2_name": {
        "city_1_name": {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    89.012,
                    -123.4567
                ]
            },
            "count": 11
        },
        "etc":"..."
    }
}
```
>This is a dictionary with each `country` as a key that gives access to another dictionary that uses `city` as a key. Using the same method I discussed in class, we use the dictionary to count individual instances (occurrences) of key words. So for every row in the database, I use the `country` to access the "country" dictionary, then use `city` to find the correct "city" dictionary, and then finally increment the `count` entry. Since `city` had over 6000 unknowns, by using `country` as a key, at least we know which country the attack occured in. 


```python
import sys
EPSILON = sys.float_info.epsilon  # smallest possible difference

def convert_to_rgb(minval, maxval, val, colors):
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

if __name__ == '__main__':
    minval, maxval = 1, 3
    steps = 10
    delta = float(maxval-minval) / steps
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
    print('  Val       R    B    G')
    for i in range(steps+1):
        val = minval + i*delta
        r, g, b = convert_to_rgb(minval, maxval, val, colors)
        print('{:.3f} -> ({:3d}, {:3d}, {:3d})'.format(val, r, g, b))
```

#### Function Output

|Val     |  R   |   G  |  B   |
|-------:|----:|----:|----:|
| 1.000 | 0 | 0 | 255 | 
| 1.200  | 0 |   50 |  204 | 
| 1.400  | 0 |  101 |  153 | 
| 1.600  | 0 | 153 |  101 | 
| 1.800  | 0 |  204 |   50 | 
| 2.000 | 0 |  255 |    0 | 
| 2.200  | 51 |  203 |    0 | 
| 2.400  | 102 |  152 |   0 | 
| 2.600  | 153 |  101 |    0 | 
| 2.800  | 203 |   51 |    0 | 
| 3.000 | 255 |    0 |    0 | 

#### Function Colors

![](https://i.stack.imgur.com/DXgTs.png)

<sup>Source: 
https://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map </sup>
