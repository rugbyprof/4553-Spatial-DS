NOT DONE
## Program 3
#### Due: 28 Sep by Midnight

### Overview:

Using the code from [here](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/geo.py) create an animated page that displays 
at least 3 polygons and 3 points where the points will change color when they are "inside" a polygon, and the polygons will change 
direction when they "collide" with another polygon. 

How you perform the collision is up to you, but one simple way is the calculate the MBR (minimum bounding rectangle) for each polygon

### Requirements:

- Your code must be fully commented
- You must 

### Commenting Code
Every program should have a comment block at the top similar to the following:

```python
"""
@author - First Last
@date -  mm/dd/yyyy
@description - This program does ..... and write more than one line ..... 

@resources - I found code and methods at http://pythonhelper.com and used some polygon code.
"""
```

Every method (or function) should have a comment block similar to the following:

```python
"""
@function NameOfFunction 

Function description ...

Found help at http://pythonsnippet.org/blah/blah and used a polygon distance function

@param  {paramType} - paramName: descriptiong
@param  {paramType} - paramName: descriptiong
@returns{retType}   - return description
"""
```

### Deliverables

1. Create a folder called `Program3` and place it in your repository.
2. Add the file `animate_poly.py` and place it in your new folder.
3. Ensure your code is fully commented. 


***Everything needs to be in your repository, named as specified, or it won't be graded.***


#### Timing a program 

Left over from last assignment, but it's always good to have.

```python
import time

start_time = time.time()

# Do all of your processing

print("Program ran in %s seconds." % (time.time() - start_time))
```

