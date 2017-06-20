Program 3 Starter Files
=======================

## Earthquake Example 

### Usage of Files

1. run `pip install requests` to install correct library for getting files.
1. run `get_quake_points.py` 
    - `python get_quake_points.py` 
    - You can adjust how much data by creating a list of years:
        - `years = [2017] ` gives data for 2017
        - `years = [2000,2001,2002,2003,2004,2005] ` gives data for years 2000-3005
        - Right now its hard coded for magnitudes greater than 5.0, but that can be changed easily.
    - It saves a file for each year: `quake-xxxx.json` where `xxxx` is  the year
    - It also saves a condensed version, with a small subset of the original quake data:
        - `quake-xxxx-condensed.json`
2. run `adjust_quake_points.py`
    - `python adjust_quake_points.py`
    - This file reads in the condensed points and adjusts them to fit a specific screen size. 
    - It first takes the points from `lat/lon` to `x/y` using the `mercator projection` formula.
    - It also adjusts for screen size, in this case I used `1024,512` wich seems to be what the `mercator projection` formula likes. 
3. run `display_quake_points.py`
    - This simply opens `quake-xxxx-adjusted.json` and displays the points on a `1024,512` screen. 
