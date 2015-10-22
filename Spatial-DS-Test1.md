# Test 1 
### Due: Monday 26 October by 10:00 am

### Topics
- B-Trees
- Quad-Trees
- KD-Trees
- R-Trees

### Guidelines:

- You must work by yourself
- You must turn in a single printed copy of your exam, and a digital copy via email.
- Use of external resources is ok, but we will see this material again on the final.

### Example Points

Heres a list of 30 points that will be used for later questions. 

```
[(39, 21), (86, 19), (65, 5), (76, 28), (3, 9), 
 (31, 59), (43, 99), (60, 50), (42, 48), (15, 73), 
 (67, 98), (16, 34), (27, 80), (51, 77), (30, 67), 
 (82, 68), (85, 46), (89, 44), (21, 30), (5, 66), 
 (75, 29), (17, 14), (40, 90), (18, 33), (52, 64), 
 (1, 71), (88, 10), (64, 26), (96, 2), (25, 40)]
```

--

## Quad-Trees

![](https://s3.amazonaws.com/f.cl.ly/items/2r3V2g3R1L1M2p1E2025/quadex.png)

#### Q1 

- Pick 21 points from the above list to load into an initially empty point Quad-tree. 
- Pick points in an order that would create a full balanced tree. 
- If there is not a set of points that will do so, state as such.
- Drawings:
    - Show the tree state after 3 points entered
    - Show the tree state after it hits a height of 3
    - Show the final state of the tree.
- The images you turn in should resemble the example above showing both representations of the tree.


#### Q2

- Besides spatial indexing, give 3 ***descriptive*** examples of interesting uses for Quad-trees (any type of Quad-tree, not just point Quad-trees),

#### Q3

- Pick a list of values that would cause the Quad-tree to grow beyond a height of 3.
- List those values here
- If it's not possible, state why.

#### Q4

- What is the maximum height achievable given the values from above?


## KD-Trees


#### Q5 

- What is the purpose of k-D trees? How does it differ from Quad-Trees? 

#### Q6

- Place the first 11 points (as chosen from question 1) into an initially empty 2-D tree.
- Drawings:
    - Show the tree state after 3 points entered
    - Show the tree state after 5 points entered
    - Show the final state of the tree.
- You should know what the structure of the tree should look like.

#### Q7

- Combine the points from the above list into groups of 2 (4D data). Then insert those 15 values into a 4-D Tree.   
- Drawings:
    - Show the tree state after 3 points entered
    - Show the tree state after 5 points entered
    - Show the final state of the tree.
- You should know what the structure of the tree should look like.



## B-Tree

Note: According to Knuth's definition, a B-tree of order m is a tree which satisfies the following properties:
- Every node has at most m children.
- Every non-leaf node (except root) has at least ⌈m⁄2⌉ children.
- The root has at least two children if it is not a leaf node.
- A non-leaf node with k children contains k−1 keys.
- All leaves appear in the same level

#### Q8

- Describe to me the history of B-trees, and what influence they've had on other data structures. Are B-Tree's still in use today? 

#### Q9

- The list above has 30 pairs of data, or 60 values. Take the first 30 values and put it into a B-tree where ***m = 5***     
- Drawings:
    - Show the tree state after 6 points entered
    - Show the tree state after 15 points entered
    - Show the final state of the tree.
- You should know what the structure of the tree should look like.


#### Q10

- What would a contemporary size of ***m*** be? Lets say I wanted to create an index on 1 billion items. What would a good size of ***m*** be and what would the height of my B-Tree be?


## R-Tree

#### Q11

Assume: ***M = 3***

- Combine the points from the above list into groups of 2 (rectangles). Then insert those 15 rectangles into the R-Tree.   
- Drawings:
    - Show the tree state after 3 points entered
    - Show the tree state after 5 points entered
    - Show the final state of the tree.
- Your drawing should be similar to the one below:

![](https://docs.oracle.com/html/A88805_01/sdo_i11a.gif)

#### Q12

- Depending on the order in which you enter the data, can the height of our R-Tree change? 

#### Q13

- Describe each of the splitting algorithms for the traditional R-Tree and what the trade offs are for each. Which would you use and when.

