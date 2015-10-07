## Program 4
#### Due: Oct 13th by Midnight (Tuesday!)

### Overview:

Using the code from [here](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/geo.py) create an animated page that displays at least 3 polygons and 3 points where the points will change color when they are "inside" a polygon, and the polygons will change direction when they "collide" with another polygon. 

How you perform the collision is up to you, but one simple way is the calculate the MBR (minimum bounding rectangle) for each polygon and assume collision when they "overlap". This is not the best way, but the easiest to implement. 

The hard part will be making them move and change direction. I won't be to hard on you, but you need to show some effort in making this work. I thought about using a "random walk" algorithm, but that would look un-natural. I would start each obect at some random location and move them like the following:

```python
    def set_direction(self,direction):
        assert direction in ['N','NE','E','SE','S','SW','W','NW']

        self.direction = direction

    def update_position(self):
        if self.direction == "N":
            self.y -= 1
        if self.direction == "NE":
            self.y -= 1
            self.x += 1
        if self.direction == "E":
            self.x += 1
        if self.direction == "SE":
            self.x += 1
            self.y += 1
        if self.direction == "S":
            self.y += 1
        if self.direction == "SW":
            self.x -= 1
            self.y += 1
        if self.direction == "W":
            self.x -= 1
        if self.direction == "NW":
            self.y += 1
            self.x -= 1
```

This would move a point in 8 different directions and make it easy to choose a new direction. 

![](http://wfkb-geography.weebly.com/uploads/2/3/9/1/23919616/8543328_orig.gif)

### Requirements:

- Your code must be fully commented
- You must animate points to change color when "inside" a polygon
- You must animate polygons to change direction when they "collide" with other polygons.
- Nothing should go off the screen (it should change direction)
- No textures or anything are required, but would be awesome.
- You must come visit me in my office at least once before Wednesday (part of your grade).

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

1. Everything will be on gitHub
1. Create a folder called `Program3` and place it in your repository.
2. Add the file `animate_poly.py` and place it in your new folder.
3. Ensure your code is fully commented, with name block at top.


***Everything needs to be in your repository, named as specified, or it won't be graded.***



