## Worldle - Spatial Game

#### Due: 03-24-2022 (Tuesday @ 9:30 a.m.)

### Introduction

-   You've seen [wordle](https://www.nytimes.com/games/wordle/index.html)
-   You've seen [worldle](https://worldle.teuteuf.fr/)
-   And now you've seen [globle](https://globle-game.com/)
-   We are going to rip off these games and create our own version.
-   Instructions and requirements to follow.
-   The helper code for this assignment can be found:
    -   [09_ApiHelp](../Lectures/../../Lectures/09_ApiHelp/README.md)
    -   [10_WebView](../Lectures/../../Lectures/10_WebView/README.md)
-   Remember that ~~[08_GemeHelp](../Lectures/../../Lectures/08_GemeHelp/README.md)~~ is not your friend!! It has some nuggets, but it is a collection of classes and functions that solve a problem going off in a much different direction. The same goes with the ~~[07_Folium](../Lectures/../../Lectures/07_Folium/README.md)~~ folder.

## Overview

The game will be played like the following:

1. The "game" will choose a country at random. It will be unknown to the player. Lets call this the `Target`
2. The "player" will choose a country as a guess. How they enter their guess is up to you:
    - Text box where they type in a name (hoping it is spelled correctly) and submitting.
    - Drop down of all the countries (minus the ones guessed already).
    - Text box where as they start typing, auto suggestion list shows up (bonus points!)
3. After the "player" guesses, feedback from the game will tell the player the following:
    - The `distance` the guess is from the `Target`.
    - The `direction` (bearing) in the form of an arrow to the `Target`.
4. GOTO 2 until the player has found the country.

## Helper Methods

There are many helper methods included in [api.py](../Lectures/../../Lectures/09_ApiHelp/api.py) to help you achieve your goal.

### Cardinal Directions

<a href="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/cardinal_directions.png"><img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/cardinal_directions.png" width="250"></a>

This is the method that will allow you to display the proper arrow after the user makes a guess. Two country centroids (or how ever your determine distance) create a line that will have a bearing. That bearing can be changed into a cardinal direction and subsequently an `arrow` to help point the way.

More specifically: Cardinal directions are a way of descretizing decimal degrees into common directional terms. The most common ones are:

-   North = 0° or 360°
-   South = 90°
-   East = 180°
-   West = 270°

But there are more that describe even more specific directions. See the two tables below for examples arrows pointing in the approximate direction of each of the cardinal directions we have defined.

#### Degrees

|        |            |        |
| :----: | :--------: | :----: |
| 337.5° | 360° or 0° | 22.5°  |
|  315°  |            |  45°   |
|  270°  |            |  90°   |
|  225°  |            | 112.5° |
| 202.5° |    180°    |  135°  |

#### Cardinal Direction Names w/ Arrows

|                                                   |                                                 |                                                   |
| :-----------------------------------------------: | :---------------------------------------------: | :-----------------------------------------------: |
| <img src="./images/NNW.png" height="30"> <br> NNW |  <img src="./images/N.png" height="30"> <br> N  | <img src="./images/NNE.png" height="30"> <br> NNE |
|  <img src="./images/NW.png" height="25"> <br> NW  |                                                 |  <img src="./images/NE.png" height="25"> <br> NE  |
|   <img src="./images/W.png" width="30"> <br> W    |                                                 |   <img src="./images/E.png" width="30"> <br> E    |
|  <img src="./images/SW.png" height="25"> <br> SW  |                                                 |  <img src="./images/SE.png" height="25"> <br> SE  |
| <img src="./images/SSW.png" height="30"> <br> SSW | <img src="./images/S.png" height="30"> <br> NNW | <img src="./images/SSE.png" height="30"> <br> SSE |

#### Method: `cardinalDirection(bearing)`

```
This method returns a `cardinal direction` given a bearing.
Params:
   bearing (float) : value between 0-360
Returns:
   cardinal direction (string) : the string value of the direction like NNE (north north east)
```

### Other Helper Methods

#### Method: `centroid(polygon)`

```
Calculates the centroid point for a polygon (linear ring of points)
Params:
   polygon (list)  : List of lon/lat points representing a polygon
Returns:
   tuple : (x,y) or lon,lat coords representing the center point
```

#### Method: `compass_bearing(pointA, pointB)`

```
Calculates the bearing between two points.
   The formulae used is the following:
      θ = atan2(sin(Δlong).cos(lat2),cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
Source:
   https://gist.github.com/jeromer/2005586
Params:
   pointA  : The tuple representing the latitude/longitude for the first point. Latitude and longitude must be in decimal degrees
   pointB  : The tuple representing the latitude/longitude for the second point. Latitude and longitude must be in decimal degrees
Returns:
   (float) : The bearing in degrees
```

#### Method: `countryCentroid(name)`

```
Get the centroid of a country by finding the largest polygon and
   calculating the centroid on that polygon only
Params:
   name (string): name of country
Returns:
   (tuple): point (x,y)
```

#### Method: `countryPoly(country)`

```
Grab the country polygon from the country "DB" (really a country reader class I wrote for you guys).
Params:
   country (string)   : name of the country you want the polygon for
Returns:
   polygon (feature/dict) : feature pulled from the countries feature collection.
```

#### Method: `DistancePointLine(px, py, x1, y1, x2, y2)`

_Might not need to use this unless you do the distance we discussed in class._

```
Calculates the distance from a given point (px,py), to the line segment (x1,y1) , (x2,y2).
Params:
   px (float) : decimal degrees longitude of point
   py (float) : decimal degrees latitude of point
   x1 (float) : decimal degrees longitude of line start
   y1 (float) : decimal degrees latitude of line start
   x1 (float) : decimal degrees longitude of line end
   y1 (float) : decimal degrees latitude of line end
Returns:
   distanc (float) : distance from point to line segment

```

#### Method: `haversineDistance(lon1, lat1, lon2, lat2, units="miles")`

```
Calculate the great circle distance in kilometers between two points on the earth (start and end) where each point
   is specified in decimal degrees.
Params:
   lon1  (float)  : decimel degrees longitude of start (x value)
   lat1  (float)  : decimel degrees latitude of start (y value)
   lon2  (float)  : decimel degrees longitude of end (x value)
   lat3  (float)  : decimel degrees latitude of end (y value)
   units (string) : miles or km depending on what you want the answer to be in
Returns:
   distance (float) : distance in whichever units chosen
```

#### Method: `largestPoly(polygons)`

```
Simple implementation to grab the "hopefully" biggest polygon for a country
   (aside from island nations / arcapelligos) that represents the "actual" country.
Params:
   polygons (list) : list of polygons
Returns:
   list : the biggest polygon in the list
```

#### Method: `lineMagnitude(x1, y1, x2, y2)`

_Might not need to use this unless you do the distance we discussed in class._

```
Calculate the magnitude of a line. This is a type of distance function. Not the same as `haversine` but is used
   in conjunction the the `DistancePointLine` method below.
   Source: https://maprantala.com/2010/05/16/measuring-distance-from-a-point-to-a-line-segment-in-python/
Params:
   x1 (float) : decimal degrees longitude of line start
   y1 (float) : decimal degrees latitude of line start
   x1 (float) : decimal degrees longitude of line end
   y1 (float) : decimal degrees latitude of line end
Returns:
   Magnitude (float) of the line (aka distance).
```

## Helper Routes

Here is a list of routes already written for you with the api code:

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/routes_available_spatial_api.png" width="800">

Each of these routes has documentation and examples so you can either use them, or write your own.

## Example Run

My run I kept bare bones, and didn't change colors on the map itself. Try and show which country was picked in relation to the table.

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/example_run.png" width="800">
