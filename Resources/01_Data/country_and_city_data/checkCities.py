""" This file checks to make sure that the csv file that is processed contains at least one city in 
each of the 50 states to make sure that the data is usable for program 1.

Also, consider this helper / example code to give you some "how-tos" on opening, reading, and a little
bit of data processing.
"""

from rich import print
import math

# These lines let me change my working directory. I only use this when I'm
# using VSCode and the base directory isn't where I'm running scripts.
# This will error if you run it on repl.it or on your computer (unless you have
# the exact same path as below.) You can comment it out, or delete it. 
import os
os.chdir("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data")
### 

""" 
Open file to be checked and read into a data variable without using pythons csv library.
readlines() reads an entire file into an list, one line per list entry. If we run the 
lines below, data would contain: 
 
data[0] = rank,state,city,latitude,longitude,population,growth
data[1] = 1,New York,New York,40.7127837,-74.0059413,8405837,4.8
data[2] = 2,California,Los Angeles,34.0522342,-118.2436849,3884307,4.8
...
""" 
with open("cities_latlon_w_pop.csv") as f:
    data = f.readlines()

# Grab column headers from data[0] then delete them from the data variable
keys = data[0]
del data[0]

# create a dictionary of states. I will be using state names as dictionary keys
# so I can count the number of cities in each state
states = {}

# loop over all 1000 rows of data
for row in data:

    # split on commas putting each data element in a list
    # strip() cleans whitespace of front a back of a string (spaces newlines tabs etc.)
    # items is now a list containing the values for: [rank,state,city,latitude,longitude,population,growth]
    items = row.strip().split(",")

    # if the state name is not a key in the dictionary, add it
    # and point it to an empty list (for counting city entries)
    if not items[1] in states:
        states[items[1]] = []
    
    # add a city to the list of the corresponding state (to count them)
    states[items[1]].append(items[0])

# print out the results with counts of how many cities in top 1000 in each state
for key,value in states.items():
    print(f"{key},{len(value)}")


# print len of dictionary should be 51 (including District of Columbia)
print(len(states))