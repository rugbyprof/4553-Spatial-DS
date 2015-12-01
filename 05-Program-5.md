## Program 5
#### Due: Dec 1st 

### Overview:

We are going to implement the A* pathfinding algorithm as the basis of a route planning program. The program should find the shortest path from a given start node to an end node. Basically, from city A to city B. We won't get extremely specific since our underlying road network is made up of primary and secondary roads (basically highways).

The road network will be represented as a weighted directed graph stored in 3 files.

#### nodes.csv

A comma seperated file with the following format:

| id | start_lat | start_lon | end_lat | end_lon | rttype | mtfcc | fullname | state | contiguous_us | distance |
|-----|----------|-----------|---------|---------|--------|-------|----------|-------|---------------|----------|
| 202448 | 34.417095184 |-96.100433350| 34.421733856| -96.094802856| M |S1200| N 69 Hwy  | OK| Y |222.69 |

#### edges.csv

A comma seperated file with the following format:

| fromID | toID |
|--------|------|
|   123  |   456|


#### nodegeometry.csv

| id | geometry |
|--------|------|
|   123  | [["-96.100431","34.417097"],...,["-96.09831199999999","34.419066"]]|


### Requirements:
- Create a graph structure using the nodes and edges files. 
- Apply the A* algorithm to the graph structure to find a shortest path between 2 nodes. 
- Show your chosen path by drawing it on a map. 

Notes:
- With the given data there might not be a path between each and every node.
- Your code must be fully commented.



### Deliverables

- A folder called `ProjAstar` should contain all your files
- In `ProjAstar` create a file called `driver.py` to run your path finding algorithm. 
- Any other files used should be in your folder.


***Everything needs to be in your repository, named as specified, or it won't be graded.***


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

@param  {paramType} - paramName: description
@param  {paramType} - paramName: description
@returns{retType}   - return description
"""
```
