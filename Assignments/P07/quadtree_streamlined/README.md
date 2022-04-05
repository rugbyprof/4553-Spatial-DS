## QuadTree 

- Simple implementation of a quadtree gotten from here: https://scipython.com/blog/quadtrees-2-implementation-in-python/
- Made minor changes
- Be careful!! Rectangles are defined cx,cy,w,h where:
  - cx is "center" x
  - cy is "center" y
  - w and h are width and height

So if you make a rectangle like (0,0,100,100) it will end up with coords:
(-50,-50,50,50).