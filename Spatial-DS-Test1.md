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

- What is the purpose of k-D trees?
- Explain how a 2-D tree extends a binary search tree.
- What is the time required to construct a k-D tree for n objects?
- Insert the following pairs (in the order shown) into an initially empty 2-D tree.

|  (53, 14)  |  (27, 28)  |  (30, 11)  |  (67, 51)  |  (70, 3)  |
|:----------:|:----------:|:----------:|:----------:|:---------:|
|     0      |     1      |     2      |     3      |     4     |
    
- Insert the following triples (in the order shown) into an initially empty 3-D tree.


|  (16, 8, 12)  |  (18, 7, 15)  |  (10, 9, 3)  |  (13, 8, 9)  |  (20, 10, 6)  |  (3, 10, 7)  |  (12, 14, 6)  |
|:-------------:|:-------------:|:------------:|:------------:|:-------------:|:------------:|:-------------:|
|       0       |       1       |      2       |      3       |       4       |      5       |       6       |
    


- Build a balanced kd-tree (nodes and edges) for the points in the figure below.
- Draw the separating planes in the figure below.
- Highlight the tree edges traversed when looking for the point with minimum x-coordinate.
- Make another copy of the tree and highlight the edges traversed when looking for points within 3 units of
(16, 6) 

![](https://s3.amazonaws.com/f.cl.ly/items/2P101P0X2Y0m0l1Q1U1Z/Screen%20Shot%202015-10-06%20at%204.19.58%20PM.png)

### R-Tree

- Briefly describe how to insert a node into an R-tree.
- Describe the Quadratic Method to split a node in an R-tree. Why is the complexity of this
method O(M<sup>2</sup>), where M is the order of the R-tree.

- Discuss the usefulness of R-trees.

- Discuss how the R-tree search is conducted.

- Why does one say that an R-tree search is not bounded in the sense that a B-tree search is bounded.

- Given some spatial data (a set of rectangles) construct an R-tree for the  data. (Be sure to satisfy the property of minimizing the dimensions of the internal nodes).

### B-Tree

#### Complexity
|        | Average   | Worst case   |
|:-------|:----------|:-------------|
| Space  | O(n)      | O(n)         |
| Search | O(log n)  | O(log n)     |
| Insert | O(log n)  | O(log n)     |
| Delete | O(log n)  | O(log n)     |

--

- What is the maximum search time in a B-Tree?


- Grow a B-tree of order 4 (i.e., a 2-3-4 tree), with the following sequence of key values:

|  1  |  15  |   10  |   4  |   8  |   9  |   5  |   2  |   7  |
|:---:|:----:|:-----:|:----:|:----:|:----:|:----:|:----:|:----:|
|  0  |  1   |   2   |  3   |  4   |  5   |  6   |  7   |  8   |