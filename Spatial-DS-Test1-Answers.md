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

>#### Answer:
>Assuming 1 point per Quad, there are not 21 points that can be picked via a visual inspection that would result in a full complete quad-tree.

>Remember a complete tree is a tree filled in from left to right, and a full tree is one in which every node has all its children:

>![](http://www.csie.ntnu.edu.tw/~u91029/BinaryTree2.png)
>
>#### Final Tree:
>![](https://s3.amazonaws.com/f.cl.ly/items/3R1g3l3r0y3H2a2E3a2W/Screen%20Shot%202015-11-03%20at%2010.24.28%20AM.png)

#### Q2

- Besides spatial indexing, give 3 ***descriptive*** examples of interesting uses for Quad-trees (any type of Quad-tree, not just point Quad-trees).

>#### Answer:
- Collision Detection
    - Discussed in class.
- Picture Representation
    - Erasing a picture takes only one step. All that is required is to set the root node to neutral.
    - Zooming to a particular quadrant in the tree is a one step operation.
    - To reduce the complexity of the image, it suffices to remove the final level of nodes.
    - Accessing particular regions of the image is a very fast operation. This is useful for updating certain regions of an image, perhaps for an environment with multiple windows.
- - Terrain rendering
    - Much like picture rendering above, in computer games the terrain needs to gain in detail as you approach specific regions, and lessen in detail as you leave. Zooming in to a specific quadrant, or zooming out will allow you to do this.

#### Q3

- Pick a list of values that would cause the Quad-tree to grow beyond a height of 3.
- List those values here
- If it's not possible, state why.

>#### Answer:
> Any two points that are very close together would cause the tree to divide the existing space enough to go beyond a height of 3. Check it out here: http://cs2.mwsu.edu/~griffin/spatial_data_graphviz/quadtree.html


#### Q4

- What is the maximum height achievable given the values from above?

> Inserting values into the quadtree (regardless of order) results in the same quadtree. Therefore by placing all 30 points into the tree we acheive a height of 6.

## KD-Trees


#### Q5

- What is the purpose of k-D trees? How does it differ from Quad-Trees?

> #### Answer:
The purpose of a K-D Tree is the same as a Quadtree. It's meant to store multi-dimensional (or spatial) data. The main difference is that a KD-Tree works much better with higher dimensional data. In Quadtrees the data reaching a node is split into a fixed (2<sup>d</sup>) (d=dimension) equal size cells, whereas in K-D Trees, the data is split into two regions based on the **discriminator**. Quadtrees do not scale well to high dimensions, due to the exponential dependency in the dimension. For example a Quadtree has 4 children for every 2D point, and would have 8 children for every 3D value (see Oct-Trees) and so on. K-D Trees aren't effected by dimension because using the discriminator value to split on results in each node having at most 2 children. 
>
In summary: K-D Tree scales well with higher dimensions. Quadtrees, not so much. 


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

>#### Answer: 
>Can't describe it any better than here: https://www.perforce.com/blog/110928/short-history-btree


#### Q9

- The list above has 30 pairs of data, or 60 values. Take the first 30 values and put it into a B-tree where ***m = 5***
- Drawings:
    - Show the tree state after 6 points entered
    - Show the tree state after 15 points entered
    - Show the final state of the tree.
- You should know what the structure of the tree should look like.

6 Items:

![](https://s3.amazonaws.com/f.cl.ly/items/161H270P2A3V100d0G3N/Screen%20Shot%202015-11-03%20at%201.38.48%20PM.png)

15 Items:

![](https://s3.amazonaws.com/f.cl.ly/items/2t0r0S472A233C2i2w31/Screen%20Shot%202015-11-03%20at%201.36.54%20PM.png)

30 Items: 
![](https://s3.amazonaws.com/f.cl.ly/items/1R301K0i210D3d01360r/test1-btree.png)

#### Q10

- What would a contemporary size of ***m*** be? Lets say I wanted to create an index on 1 billion items. What would a good size of ***m*** be and what would the height of my B-Tree be?

>####Answer:
>The original goal of a B-Tree was to index data (speed up searches) that was too large to fit entirely into memory. Since some of the data resided on disk, the inner nodes of a B-Tree could reside in memory, and the leaf nodes could literally be associated with disk pages. SO, a good choice of ***m*** would correspond to the number of values that could fit into disk page (or disk block, or swap page). Many years ago disk blocks were 512K and nowadays were looking at 4096K or 2<sup>12</sup>. 
>
>If were looking to keep a B-Tree in memory (not really it's purpose) we might want to make sure ***m*** corresponds with cache size (or least < than cache size). 

Good article on disks: http://pclt.sites.yale.edu/blog/2010/03/10/disk-block-size

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

> Nope. An R-Tree is similar to a B-Tree such that all leafs are at the same level, meaning it is a height balanced tree regardless of order of insertion. 

#### Q13

- Describe each of the splitting algorithms for the traditional R-Tree and what the trade offs are for each. Which would you use and when.

>####Answer: 
>- Exhaustive
    - Best result
    - Most cost
- Quadratic
   - decent result
   - some cost
- Linear
   - no guarantees
   - best cost
   
> Quadratic is probably a good tradeoff between speed and performance.

