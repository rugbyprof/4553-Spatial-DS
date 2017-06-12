Program 1 - Drawing Countries
=========
hello tam
### Due: Wednesday Jun 14th by Classtime


### Overview

There is a starter code package [HERE](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Resources/Pygame/10-basic_geo_draw.py) that contains the following classes:

| Class Name     | Description       |
|:---------------|:----------------------------------------------------------------------------------|
| Colors         | Returns (r,g,b) tuples given a color name.   |
| StateBorders    | Returns polygons given a state name or code. Can return all states.   |
| WorldCountries  | Same as states, but for countries.    |
| DrawGeoJson     | Converts lat/lon to x,y and scales it (kind of) to a printable flat space. |
| DrawingFacade   | A helper class that makes interacting with the above classes easier . |

- If you run it, it will draw a few polygons to a pygame window. 

<img src="https://d3vv6lp55qjaqc.cloudfront.net/items/3n0e09001d2f2Y1y3d0k/Screenshot%202017-06-12%2014.17.16.png" width="500">

- Running your mouse over the window will continuously change the country colors (annoying, but shows use of color class and random colors). 

### Requirements

Your job is to add the following functionality to this program:
1. Capture mouse click.
2. Determine which polygon contains the click (if any).
3. Border that polygon with a thick black border.
4. Print the countries name or states name somewhere on the screen (preferrably on the polygon).
5. Draw bounding box rectangle around the country or state you clicked.

### Deliverables

1. Create a folder called `Program_1` in your `Assignments` folder.
2. Copy the [Starter Code](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Resources/Pygame/10-basic_geo_draw.py) into `main.py`
3. Add the proper functionality based on the requirements. 
4. Bring a printout of `main.py` to class on day due.
5. Print out a screen shot of output showing requirements met. 
