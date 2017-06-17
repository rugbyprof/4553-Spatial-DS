Program 2 - DBscan
=========

*** NOT DONE ! ***

### Due: Monday Jun 19th by Classtime


### Overview

Use Pygame to create a 2D scatterplot of locations of crimes. Each point should be color coded to match the actual crime committed. Run DBscan on your data to find high crime areas. You can either read in the Lat/Lon data and use our projection code to convert to x/y, or you can use the existing x,y that is included in the data set. Either way, your going to have to scale the points so that they don't cluster (no pun inteaded) in one portion of the screen. Below is an example dividing each x/y from the dataset by 1000:

|       |
|:------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/0b111F2h3k0f3i1T2x2l/%5Baf6c80974353cb65e2d1a0d7c9578d8a%5D_Screenshot%25202017-06-15%252017.47.11.png?X-CloudApp-Visitor-Id=1094421) |
| Example output w/out scaling points to screen |

The points ***must*** be scaled so that visualization of unique clusters will not be a chore. 

|       |
|:------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/28462H2A361E0r3F0K14/Screenshot%202017-06-15%2019.23.55.png?X-CloudApp-Visitor-Id=1094421) |
| Example output with scaling points to screen |

|       |
|:------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/20121R0e3Y3T2u2P2Q45/screen_shot_400x.png) |
| Example output showing all 5 buroughs in different colors |

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

### Requirements

- Plot the points from all five buroughs on seperate screens.
- Use `pygame.image.save(screen , path_to_image)` to save your screen to a 'png' formatted image named `crimes_burough_name.png`. 
- Make the screen size 2000x2000. This may look poor on your individual machines, but by saving the screen to an image will make it easily viewable.
- Use the minimum and maximum coordinate values from all 5 files. If you simply process one file at a time, it will spread the points out within the entire 2000x2000 screen, and we want to see each burough in relation to the others. Here are the extreme coords:
    - MaxX: 1067226
    - MaxY: 271820
    - MinX: 913357
    - MinY: 121250
    

    
- At the top right of your screen write the `burough` name 
- Set your `eps` and `min` pts to values that create many small clusters. If I can, I will post an example of my output.
- Color the points so that:
     - LARCENY       = BLUE (0,0,255)
     - ASSAULT       = RED (255,0,0)
     - HARRASSMENT   = GREEN (0,255,0)
     - DRUGS         = YELLOW (255,255,0)
     - VEHICLE FRAUD = PURPLE (128,0,128)
- Extra credit if you color the 
