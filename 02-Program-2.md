## Program 2A
#### Due: 22 Sep by Midnight

### Overview:

Using the starter kd-tree [here](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/kd-tree-simple.py) write some code to help us visualize our tree. 

A kd-tree is a multi-dimensional tree, however it's structure is bounded by a node having from 0 to 2 children. Drawing
a binary tree is not necessarily difficult, but graphviz will help us tremendously. 

```python
import graphviz as gv
g1 = gv.Graph(format='svg')
g1.node('A')
g1.node('B')
g1.edge('A', 'B')
```

Will create the following:
![](http://f.cl.ly/items/0i071C3T3j0Y2R0j2Y3h/g1.png)

Changing 
`g1 = gv.Graph(format='svg')` to `g1 = gv.Digraph(format='svg')` will create a directed graph instead.

```python
import graphviz as gv
g1 = gv.Digraph(format='svg')
g1.node('A')
g1.node('B')
g1.node('C')
g1.edge('A', 'B')
g1.edge('A', 'C')
g1.edge('B', 'C')
```
![](http://f.cl.ly/items/0B0v2j2r0n0L3g2o2H2f/g4.png)

```python
import graphviz as gv
g1 = gv.Digraph(format='svg')
g1.node('A',{'label': 'Node A'})
g1.node('B',{'label': 'Node B'})
g1.node('C')
g1.edge('A', 'B',{'label': 'Edge 1'})
g1.edge('A', 'C',{'label': 'Edge 2'})
g1.edge('B', 'C')
```

![](http://f.cl.ly/items/3p0c1h1E252G0i1x3b2K/g5.png)


### Requirements

- Add graphviz to your platform. On a mac simply `brew install graphviz` 
- Add graphviz as a package for python. On a mac `pip install graphviz`


### Deliverables

***Everything needs to be in your repository, named as specified, or it won't be graded.***

#### Timing a program

```python
import time

start_time = time.time()

# Do all of your processing

print("Program ran in %s seconds." % (time.time() - start_time))
```

