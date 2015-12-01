## Program 5 
#### Part 1
#### Due: Nov 20th by 5pm

### Overview:

We are going to implement the A* pathfinding algorithm as the basis of a route planning program. The program should find the shortest path from a given start node to an end node. Basically, from city A to city B. We won't get extremely specific since our underlying road network is made up of primary and secondary roads (basically highways). In this first part, we will simply read the files in utilzing `json` and `csv` libraries.


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


#### nodegeometry.json

```json
{"id":"202462","geometry":"[[ -96.391037 , 35.839709 ],[ -96.390997 , 35.84016 ],[ -96.39087699999999 , 35.840621 ],[ -96.390855 , 35.840685 ]]"}
```


### Requirements:
- Read the nodes and edges files in. 
- Be able to retreive a geometry for a node based on the id. 
- As an example, print the geometry of a node in your output. 
- Your output should look like:

```
Your Name
Program 5 - Part 1

nodes.csv read containing x nodes.
edges.csv read containging x edges.

Node x contains x points. The geometry follows:

-96.391037 , 35.839709 , 
-96.390997 , 35.84016 ,
-96.39087699999999 , 35.840621 ,
-96.390855 , 35.840685 


```

Notes:
- With the given data there might not be a path between each and every node.
- Your code must be fully commented.



### Deliverables

- A folder called `ProjAstar-1` should contain all your files
- In `ProjAstar-1` create a file called `load_files.py` to run your path finding algorithm. 
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
