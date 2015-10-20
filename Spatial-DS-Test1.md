# Not Done
In fact some questions may be chopped. I'm just gathering right now.<br>
I'll organize in the next day or two.


# Test 1 Study Guide

## Topics
- **B-Trees**
- **Quad-Trees**
- **KD-Trees**
- **R-Trees**


### KD-Trees

#### Complexity

|        | Average   | Worst case   |
|:-------|:----------|:-------------|
| Space  | O(n)      | O(n)         |
| Search | O(log n)  | O(n)         |
| Insert | O(log n)  | O(n)         |
| Delete | O(log n)  | O(n)         |

--

- Q1. What is the purpose of k-D trees?

- Q2. Explain how a 2-D tree extends a binary search tree.

- Q3. What is the time required to construct a k-D tree for n objects?

- Q4. Insert the following pairs (in the order shown) into an initially empty 2-D tree.

|  (53, 14)  |  (27, 28)  |  (30, 11)  |  (67, 51)  |  (70, 3)  |
|:----------:|:----------:|:----------:|:----------:|:---------:|
|     0      |     1      |     2      |     3      |     4     |
    
- Q5. Insert the following triples (in the order shown) into an initially empty 3-D tree.


|  (16, 8, 12)  |  (18, 7, 15)  |  (10, 9, 3)  |  (13, 8, 9)  |  (20, 10, 6)  |  (3, 10, 7)  |  (12, 14, 6)  |
|:-------------:|:-------------:|:------------:|:------------:|:-------------:|:------------:|:-------------:|
|       0       |       1       |      2       |      3       |       4       |      5       |       6       |
    


- Q6. Build a balanced kd-tree (nodes and edges) for the points in the figure below.

- Q7. Draw the separating planes in the figure below.

- Q8. Highlight the tree edges traversed when looking for the point with minimum x-coordinate.

- Q9. Make another copy of the tree and highlight the edges traversed when looking for points within 3 units of (16, 6) 

![](https://s3.amazonaws.com/f.cl.ly/items/2P101P0X2Y0m0l1Q1U1Z/Screen%20Shot%202015-10-06%20at%204.19.58%20PM.png)

### R-Tree

- Q1. Briefly describe how to insert a node into an R-tree.

- Q2. Describe the Quadratic Method to split a node in an R-tree. Why is the complexity of this method O(M<sup>2</sup>), where M is the order of the R-tree.

- Q3. Discuss the usefulness of R-trees.

- Q4. Discuss how the R-tree search is conducted.

- Q5. Why does one say that an R-tree search is not bounded in the sense that a B-tree search is bounded.

- Q6. Given some spatial data (a set of rectangles) construct an R-tree for the  data. (Be sure to satisfy the property of minimizing the dimensions of the internal nodes).

- Q7. In B-trees, a lookup for a key never needs to explore more than one path from root to child. In R-trees, this is not true. Why?

- Q8. When splitting a node in an R-tree, the rule for redistributing the entries is to minimize the resulting area of the two new nodes. What is the motivation for this rule? Give examples of how you might do this.

-  Q9. Consider the following dataset S of 16 objects in a 2-dimensional space: 
```
a=(1,3), b=(1,4), c=(2,0),  d=(1,7), 
e=(2,5), f=(2,8), g=(3,4.5),h=(3,1), 
i=(4,2), j=(4,3), k=(5,1),  l=(5,3), 
m=(6,1), n=(6,7), o=(7,0),  p=(7,1)
```
- Also, assume that you have an R-tree built on dataset ***S***, with the following nodes: 
    - The root node contains R6 and R7, 
    - R6 contains R1, R2, R3 and 
    - R7 contains R4 and R5. 
- The MBRs for each node from R1-R7 are: 
```
R1 = [(2,0), (3,1)], R2 = [(5,0), (7,1)], R3 = [(4,2), (5,3)],
R4 = [(1,3), (3,5)], R5 = [(1,7), (6,8)], R6 = [(2,0), (7,3)], 
R7 = [(1,3), (6,8)]. 
```

See the resulting R-Tree below

![](https://s3.amazonaws.com/f.cl.ly/items/340X0t031f073J3j1f1K/rtree-S.png)

Using your newly built R-Tree, give the sequence of pages searched and the results for the following queries:
- Q9a. Perform a Nearest Neighbor search for point Q1 = (3, 2.5).
- Q9b. Perform a range search with Minimum Bounding Rectangle: Q2 = [(3.5, 2),(5, 4)].

### B-Tree

#### Complexity
|        | Average   | Worst case   |
|:-------|:----------|:-------------|
| Space  | O(n)      | O(n)         |
| Search | O(log n)  | O(log n)     |
| Insert | O(log n)  | O(log n)     |
| Delete | O(log n)  | O(log n)     |

--

- Q1. What is the maximum search time in a B-Tree?


- Q2. Grow a B-tree of order 4 (i.e., a 2-3-4 tree), with the following sequence of key values:

|  1  |  15  |   10  |   4  |   8  |   9  |   5  |   2  |   7  |
|:---:|:----:|:-----:|:----:|:----:|:----:|:----:|:----:|:----:|
|  0  |  1   |   2   |  3   |  4   |  5   |  6   |  7   |  8   |

- Q3. By adding the same values to a B-Tree in a different order, do we get the same B-Tree? Draw two B-trees of order 3 where M=3 and L=3 (this just means that internal nodes have 3 pointers (M) and leafs hold 3 values (L)) Draw one for the input sequence {11, 12, 13, 14, 15, 16}, and another for the sequence {14, 11, 13, 15, 12, 16}.  Decide whether it is better to construct B-trees with ordered data or with data in some random order.
