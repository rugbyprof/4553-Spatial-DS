Heat Map
========

### Overview

Generate a heat style map showing terrorist hotspots around the world. You have a couple of choices of how to get this done:
1. Grid method 
2. Count City method

#### Grid Method

The grid method takes xy coordinates and maps then into a 2d array and counting the occurences of each cell. After all xy coordinates have been placed in a cell, take the extreme values and assign a "heat" or color using the color function below:


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

####Function Output
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



