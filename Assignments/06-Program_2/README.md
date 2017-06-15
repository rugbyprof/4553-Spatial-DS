Program 2 - DBscan
=========

### Due: Monday Jun 19th by Classtime


### Overview

Use Pygame to create a 2D scatterplot of locations of crimes. Each point should be color coded to match the actual crime committed. Run DBscan on your data to find high crime areas. You can either read in the Lat/Lon data and use our projection code to convert to x/y, or you can use the existing x,y that is included in the data set. Either way, your going to have to scale the points so that they don't cluster (no pun inteaded) in one portion of the screen. Below is an example dividing each x/y from the dataset by 1000:

|       |
|:------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/0b111F2h3k0f3i1T2x2l/%5Baf6c80974353cb65e2d1a0d7c9578d8a%5D_Screenshot%25202017-06-15%252017.47.11.png?X-CloudApp-Visitor-Id=1094421) |
| Example output w/out scaling points to screen |

There is a starter code package [HERE](https://github.com/rugbyprof/4553-Spatial-DS/tree/master/Resources/Dbscan_Ex) that contains the following files:

- dbscan.py (DBscan implementation)
- main.py (driver file to show basic usage)


There is another folder [HERE](https://github.com/rugbyprof/4553-Spatial-DS/tree/master/Resources/NYPD_CrimeData)  that holds a bunch of NY City crime data. 

