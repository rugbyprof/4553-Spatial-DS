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
- This is PSEUDO code ... it does NOT run

**Create Grid**
```
grid = [][]
for each (lon,lat) in list:
  x,y = adjusted(lon,lat)
  grid[x][y]++
end
```
>This would create your grid. Rows and columns would need to be figured out before hand
based on screen size, and number of data points (for visual effect). Remember, with more
cells a finer grained heat map is created. Less cells would create large blocks of 
color.

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

<sup>Source: 
https://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map </sup>
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

