Heat Map
========
### Due Friday 7 Jul by Midnight.

## Overview

Generate a heat style map showing terrorist hotspots around the world. You have a couple of choices of how to process the data:
1. Adjusting lon,lat coordinates and mapping them to a cell (bucket).
2. Counting Cities, and then doing the above based on a cities coordinates. :)

### Creating Your Grid

The grid method takes the geometry of each occurence and after converting the coordinates to xy values, it maps them into a 2d array (x val = row index and y val = column index). Every time a coordinate maps to a cell, simply increase the value of that cell by one, keeping a count. The number of occurences of each cell will be assigned a color value based on the function below, where the highest occuring value will get assigned the "hottest" color (red), and the least occuring values will get assigned the "coolest" color (blue).

How you display your grids on the map is up to you. You could represent each grid cell as a box or rectangle thereby coloring the area of the map that it represented. Or, you could use another shape or icon and change the color and or size based on its value. As long as your visual output makes it very apparent where the "hot spots" are.  

#### Steps for Create Grid

1. Create some ***`MxN`*** grid (most likely your screen size: 1024x512 )
2. Process each record in data set.
3. Map each record to some grid cell: grid[ ***`m`*** ][ ***`n`*** ] using the geometry of each record.
    - Method 1 = convert lat/lon to x/y and then map to grid[x][y] (our mercator method gives us x=[0,1024] and y=[0,512] (adjusting for our image size).
    - Method 2 = convert lat/lon to some integer range of buckets (described below).
4. Increment the cell value by 1 every time a coordinate maps to it. 
5. Highest count value gets hottest color and Lowest count value gets coolest color. (function below)
6. Draw the grid colors on the map in the appropriate location (the row,col location IS the x,y location on the map)
7. How you draw the colors on the map is up to you (sqaures, circles, increase size based on color, icons, etc.)

**Create Grid pseudo code**
```
grid = [][]
for each (lon,lat) in list:
  x,y = adjusted(lon,lat)
  grid[x][y]++
end

# or

grid = [][]
city_count = {} (some dictionary)
for each (city,count) in city_count:
  x,y = get_adjusted_city(lon,lat)
  grid[x][y] = count
end
```
<sub>This is PSEUDO code ... it does NOT run</sub>
>This would create your grid. Rows and columns would need to be figured out before hand
based on screen size, and number of data points (for visual effect). 

--------

We could place lat/lon values into buckets instead of using the adjusted x,y coordinates. The table below tells us how precise a lat,lon coordinate is based on how many decimal places it contains. We only need a bout 2 places of precision if we use a grid size representing our screen size. 

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

The `terrorism collection` contains the following precision where key = precision (decimal places) and value = count. So the majority of the collection (120000+) contain 6 decimals or more. This is only relevant
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

If you just print out small points of color based your values in your newly created grid of values, you may not get the effect we want. Especially since most of our counts of attacks will be pretty localized. You can use the method below to expand or "blur" your color values to give more of a desired effect. The more passes you make, the larger the blur (larger != better). Some blurring I think could help depending on how you decide to display your output.

| Bad  |  Good       |
|:------:|:--------:|
|![](https://d3vv6lp55qjaqc.cloudfront.net/items/231o1f3A1O3d0B3Z1R2G/heat_map2.png) | ![](https://d3vv6lp55qjaqc.cloudfront.net/items/1V3G0N2t1Z3E3D2o3Q1G/heat_map.png ) | |
|         |         |


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

- <sup>Source: https://stackoverflow.com/questions/2343681/algorithm-for-heat-map</sup>

#### Count Cities

No matter what, we will have to use the geometries from each record and count all occurrences. If you want to obtain the counts of attacks by city, this can be a shortcut, but there are 6000 records that have city listed as "unknown". If this were a long semester, we could "[geocode](https://en.wikipedia.org/wiki/Geocoding)" the coordinates to get closest city.  

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

### Color Mapping 

After your 2D grid is created, you could use the following function to obtain a color value based on the count of occurences in a given cell. Again, it's up to you how you display your heat map, however, it should be easy to see your map.

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

### Deliverables

- Create a folder called `program_6` in your assignments folder.
- Your heat map generating file should be called `heat_map.py`.
- Any files you use in conjunction with `heat_map.py` should be included in this folder. 
- I should be able to run your code after downloading your project folder with little or no changes. 
- Code should be commented based on [this](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Resources/example_commenting.md)

