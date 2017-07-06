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

>This would create your grid. Rows and columns would need to be figured out before hand
based on screen size, and number of data points (for visual effect). Remember, with more
cells a finer grained heat map is created. Less cells would create large blocks of 
color.
>```
grid = [][]
for each (lon,lat) in list:
  x,y = adjusted(lon,lat)
  grid[x][y]++
end
```

There are other algorithms to "blur" a 2D array of pixels (gaussian most popular), 
but here is a method to let a strong (high heat) value bleed into neighboring cells.
This technique would work best with lots of cells. 

- The idea is to pass over the grid ___`N`___ number of times. 
- Each pass adds 1 to the current cell value.
- You could also increment "adjacent" cells with each pass. 
    - Adjacent = 8 neighboring cells. 
- Depending on the number of passes, your "hot" areas will expand accordingly.

```
for 0 to # of passes
  for each row
   for each col
     if grid[row,col] > 0 then
       grid[row,col] += 1
       increment_adjacent_cells(row, col)
     end
   end
  end
end
```


#### Count Cities

This method simply uses the "city' name to count the number of occurences around the world. A problem with this method is that the "city" value is "unknown" for over 6000 entries. So, here .....


After all xy coordinates have been placed in a cell, take the extreme values and assign a "heat" or color using the color function below:

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

