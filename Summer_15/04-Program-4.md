## Program 4
#### Due: Oct 18th by Midnight (Sunday)

### Overview:

- Perform collision detection on a set of `N` constantly moving balls in some `W x H` window so that:
    - the balls change direction when two or more balls try to occupy the same space.
    - the balls either bounce off of the walls OR are transferred to the opposite side of the screen and travelling in the same direction. 
- N should be at minimum 5, and a maximum is up to you. Performance will obviously degrade if N gets very large. 
- The size of your browser window is also up to you, but you will be able to test more efficiently if you use a small N in a reduced window size.

- I created an entire quadtree repo here that tracks balls with a quadtree and displays the boundaries along with the balls.
- All you would need to do is make sure you can use the tree to check for collisions. (we will discuss this in class).
- https://github.com/rugbyprof/quadtree_example

### Requirements:
- Using a data structure to reduce the number of comparisons is a must. 
- Balls that collide should change color and grow.
- Nothing should go off the screen (it should change direction)
- You must come visit me in my office at least once on or before Tuesday the 13th (part of your grade).
- Your code must be fully commented.

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
1. Create a folder called `Program4` and place it in your repository.
2. Add the file `collision.py` and place it in your new folder.
3. Ensure your code is fully commented, with name block at top.


***Everything needs to be in your repository, named as specified, or it won't be graded.***



