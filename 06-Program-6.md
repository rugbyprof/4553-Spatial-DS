## Program 6
#### Part 1
#### Due: Sun 6th by Midnight

### Overview:

I put a working version of an Astar implementation that I got from [here](https://gist.bestyiwan.com/jdp/1687840) on our repo. I did somewhat integrate it with pantograph, but not fully. That's going to be the final assignment, completing my nearly complete implementation. You can see it here: https://github.com/rugbyprof/4553-Spatial-DS/tree/master/Astar.



#### No OSM or LeafJs

Sadly I couldn't create a clean viable graph with enough connections, and big enough to make it interesting, for you to run Astar on. I did learn that shape files have zero guarantee on the direction of a road segment. I'm confident in stating this based on: https://plugins.qgis.org/plugins/lineswitch/ (A whole QGis plugin written to change their direction) and a decent article on how to visualize segments better  ... all for the purpose of detecting wrong direction http://woostuff.wordpress.com/2012/07/22/qgis-style-tricks-using-styles-to-help-fix-kerb-line-directions/ . Anyway, here's the runner up program. Booo.

### Requirements:
IN CLASS


### Deliverables
- Copy the Astar starter code. 
- Create a folder called `NoGisAstar` and place the files in it. The only one you really need from the folder is `example_grid.py`. Copy that one and change the name to `AstaroGraph.py`
- As always, when finished with the deliverables, place all your files in your repo and commit.
- Fully commmented code.



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
