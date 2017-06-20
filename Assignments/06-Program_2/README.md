Program 2 - DBscan
=========

### Due: Monday Jun 19th by Classtime

### Overview

Use Pygame to create a 2D scatterplot of locations of crimes. Each point should be color coded to match the actual crime committed. ~~Run DBscan on your data to find high crime areas.~~ You can either read in the Lat/Lon data and use our projection code to convert to x/y, or you can use the existing x,y that is included in the data set. Either way, your going to have to scale the points so that they don't cluster (no pun inteaded) in one portion of the screen. Below is an example of dividing the x/y points by 1000 to give them a value that would plot to our image size, but __without any scaling__:

|       |
|:------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/0b111F2h3k0f3i1T2x2l/%5Baf6c80974353cb65e2d1a0d7c9578d8a%5D_Screenshot%25202017-06-15%252017.47.11.png?X-CloudApp-Visitor-Id=1094421) |
| Example output w/out scaling points to screen |

The points ***must*** be scaled so that visualization of unique clusters will not be a chore. You can use this formula, found [HERE](https://en.wikipedia.org/wiki/Feature_scaling) to get your points scaled correctly:

|       |
|:------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/2P150Z2E3y0l1u0H1v17/Screenshot%202017-06-15%2019.20.16.png) |
| Formula to scale values to some range.|

|       |       |
|:------:|:------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/461T0v0q272z3k0M1f2c/screen_shot_400x-bw.png) | ![](https://d3vv6lp55qjaqc.cloudfront.net/items/1j3R3y2n1c1Q3c0A2R0p/screen_shot_400.png) |
| Example output with scaling points to screen, w/out inverting y coords  |Example output showing all 5 buroughs in different colors |

There is a starter code package [HERE](https://github.com/rugbyprof/4553-Spatial-DS/tree/master/Resources/Dbscan_Ex) that contains the following files:

- dbscan.py (DBscan implementation)
- main.py (driver file to show basic usage)


There is another folder [HERE](https://github.com/rugbyprof/4553-Spatial-DS/tree/master/Resources/NYPD_CrimeData)  that holds files dealing with NYC crime data. You will need to open and process the following files:

- filtered_crimes_bronx.csv
- filtered_crimes_brooklyn.csv
- filtered_crimes_manhattan.csv
- filtered_crimes_queens.csv
- filtered_crimes_staten_island.csv

Each of these files contains crimes dealing with:

 - LARCENY
 - ASSAULT
 - HARRASSMENT
 - DRUGS
 - VEHICLE FRAUD

So we will plot the above crimes for each burough in NYC. This will help keep your program resource requirements down. 

### Part 1 Requirements

- Plot the points from all five buroughs on the same screen.
- Make sure you invert your "Y" coordinate so the output matches the coorect orientation of NYC.
- ~~Use `pygame.image.save(screen , path_to_image)` to save your screen to a 'png' formatted image named `burough_name_screen_shot.png` (e.g. `bronx_screen_shot.png` or `manhattan_screen_shot.png`).~~
-  Use `pygame.image.save(screen , path_to_image)` to save your screen to a 'png' formatted image named `all_buroughs_screen_shot.png` 
- ~~Make the screen size 2000x2000. This may look poor on your individual machines, but by saving the screen to an image will make it easily viewable.~~
- Make the screen size 1000x1000.
- Use the minimum and maximum coordinate values from all 5 files as a whole. If you simply process one file at a time, it will spread the points out within the entire 2000x2000 screen, and we want to see each burough in relation to the others. Here are the extremes from all files for you to use:

```json
{
 "MaxX": 1067226,
 "MaxY": 271820,
 "MinX": 913357,
 "MinY": 121250
 }
```
   
- ~~At the top right of your screen write the `burough` name~~
- ~~Set your `eps` and `min` pts to values that create many small clusters. If I can, I will post an example of my output.~~
- ~~Color the points so that:~~
     - ~~LARCENY       = BLUE (0,0,255)~~
     - ~~ASSAULT       = RED (255,0,0)~~
     - ~~HARRASSMENT   = GREEN (0,255,0)~~
     - ~~DRUGS         = YELLOW (255,255,0)~~
     - ~~VEHICLE FRAUD = PURPLE (128,0,128)~~
- Color the points so that:
     - Manhatten       = firebrick rgb(194,35,38)
     - Queens          = tomato rgb(243,115,56)
     - Staten_Island   = goldenrod rgb(253,182,50)
     - Bronx           = teal rgb(2,120,120)
     - Brooklyn        = brown rgb(128,22,56)

#### Deliverables

- Make sure github has all your files by 5pm Monday.
  - Create a folder called `program_2` and put this into your `Assignments` folder making sure all of your files are in this folder.
- Turn the following in at the beginning of class Monday:
  - Top page is a screen shot, with your name and printout formatted like this: [example](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Assignments/06-Program_2/example_screenshot.md)
  - Print out of `main.py` (comment your code based on [this](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Resources/example_commenting.md))


