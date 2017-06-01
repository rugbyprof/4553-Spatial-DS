from math import sqrt
from itertools import product
import pantograph

"""
START Astar Implementation
Obtained from gisthub and pulled out of its own file `astar.py` to
make it a little easier to incorporate pantgraph
"""
class AStar():
    def __init__(self, graph):
        self.graph = graph
        self.moves = []

    def heuristic(self, node, start, end):
        raise NotImplementedError

    def search(self, start, end):
        openset = set()
        closedset = set()
        current = start
        openset.add(current)  #lets add the start coordinate
        while openset:  #openset still has items in it
            current = min(openset, key=lambda o:o.g + o.h)  #
            if current == end:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]   #reverse the path
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.g + current.move_cost(node)
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    node.g = current.g + current.move_cost(node)
                    node.h = self.heuristic(node, start, end)
                    node.parent = current
                    openset.add(node)
        return None

class AStarNode(object):
    def __init__(self):
        self.g = 0
        self.h = 0
        self.parent = None

    def move_cost(self, other):
        raise NotImplementedError

class AStarGrid(AStar):
    def heuristic(self, node, start, end):
        # NOTE: this is traditionally sqrt((end.x - node.x)**2 + (end.y - node.y)**2)
        # However, if you are not interested in the *actual* cost, but only relative cost,
        # then the math can be simplified.
        return abs(end.x - node.x) + abs(end.y - node.y)
        #return sqrt((end.x - node.x)**2 + (end.y - node.y)**2)

class AStarGridNode(AStarNode):
    def __init__(self, x, y):
        self.x, self.y = x, y
        super(AStarGridNode, self).__init__()

    def move_cost(self, other):
        diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
        return 14 if diagonal else 10

    def __repr__(self):
        return '(%d %d)' % (self.x, self.y)

def make_graph(mapinfo):
    nodes = [[AStarGridNode(x, y) for y in range(mapinfo['height'])] for x in range(mapinfo['width'])]

    graph = {}
    for x, y in product(range(mapinfo['width']), range(mapinfo['height'])):
        node = nodes[x][y]
        graph[node] = []
        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (0 <= x + i < mapinfo['width']): continue
            if not (0 <= y + j < mapinfo['height']): continue
            if [x+i,y+j] in mapinfo['obstacle']: continue
            graph[nodes[x][y]].append(nodes[x+i][y+j])
    return graph, nodes

"""
END Astar Implementation
"""

"""
A pantograph / Astar extension to output the results of the algorithm
visually.
"""
class DrawAstar(pantograph.PantographHandler):

    """
    Our constructor
    """
    def setup(self):
        self.block = 10                 # grid size on the browser
        self.obstacles = []             # cells in the grid to block astar
        self.adjObstacles = []          # adjusted for astar because each grid cell is "block" times big.
        self.startCoord = None          # Start Cell
        self.finishCoord = None         # Finish Cell
        self.pathFound = False          # Set path found to false so we don't try to draw it right off
        self.path = None                # Holds the found path (if any) so we can draw it.

        print self.width/self.block     #Debugging values
        print self.height/self.block

    """
    Start the Astar pathfind algorithm aka RELEASE THE KRAKEN!
    """
    def startAstar(self):
        # Initialize Astar
        graph, nodes = make_graph({"width": self.width/self.block, "height": self.height/self.block, "obstacle": self.adjObstacles})

        # Build the graph
        paths = AStarGrid(graph)

        # Pull start and finish cell coordinates off the grid
        startx,starty = self.startCoord
        finishx,finishy = self.finishCoord

        # Divide block size into the coordinates to
        # bring them back to the original state
        startx /= self.block
        starty /= self.block
        finishx /= self.block
        finishy /= self.block

        # Grab the start and end nodes (copies) from the graph
        start, end = nodes[startx][starty], nodes[finishx][finishy]

        # Start searching
        path = paths.search(start, end)
        if path is None:
            print "No path found"
        else:
            print "Path found:", path
            self.path = path
            self.pathFound = True


    #def addElement(self.element,x1,y1,x2,y2)

    """
    Continous calls to redraw necessary items
    """
    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        self.drawGrid()
        self.drawObstacles()
        self.drawStartFinish()
        if self.pathFound:
            self.drawPath()
        self.drawPatch(400,400,900,900,'brick.png')



    """
    Draw the found path
    """
    def drawPatch(self,x1,y1,x2,y2,element):
        x1,y1 = self.adjustCoords(x1,y1)
        x2,y2 = self.adjustCoords(x2,y2)

        for x in range(x1,x2,self.block):
            for y in range(y1,y2,self.block):
                self.draw_image(element,x ,y, self.block, self.block)



    """
    Draw the found path
    """
    def drawPath(self):
        for p in self.path:
            # Blow up the cordinates pulled from Astar to fit our grid
            x,y = self.adjustCoords(p.x*self.block,p.y*self.block)
            self.fill_rect(x, y, self.block , self.block , "#00F")

    """
    Draw the background grid
    """
    def drawGrid(self):
        for i in range(0,self.width,self.block):
           self.draw_line(i, 0, i, self.height, "#AAAAAA")
           self.draw_line(0, i, self.width, i , "#AAAAAA")


    """
    Toggle means that it draws an obstacle, unless you click on
    an already "obstacled" cell, then it turns off
    """
    def toggleObstacle(self,x,y):
        gridX = x
        gridY = y
        adjX = gridX / self.block
        adjY = gridY / self.block
        if [gridX,gridY] not in self.obstacles:
            self.obstacles.append([gridX,gridY])
            self.adjObstacles.append([adjX,adjY])
        else:
            self.obstacles.remove([gridX,gridY])
            self.adjObstacles.remove([adjX,adjY])
        #print self.obstacles
        #print self.adjObstacles

    """
    This version printed like 4 blocks at a time for fast
    blockage. Basically a nested loop that added  the values
    -1, 0 ,1 on subsequent iterations to fatten the obstacle.
    """
    # def toggleObstacle(self,x,y):
    #     for i in range(-self.block,self.block,self.block):
    #         for j in range(-self.block,self.block,self.block):
    #             gridX = x+i
    #             gridY = y+j
    #             adjX = gridX / self.block
    #             adjY = gridY / self.block
    #             if [gridX,gridY] not in self.obstacles:
    #                 self.obstacles.append([gridX,gridY])
    #                 self.adjObstacles.append([adjX,adjY])
    #             else:
    #                 self.obstacles.remove([gridX,gridY])
    #                 self.adjObstacles.remove([adjX,adjY])
    #             #print self.obstacles
    #             #print self.adjObstacles

    """
    Draws the obstacles :)
    """
    def drawObstacles(self):
        for r in self.obstacles:
            self.fill_rect(r[0], r[1], self.block , self.block , "#000")

    """
    Draws the start and finish coordinates
    """
    def drawStartFinish(self):
        if self.startCoord:
            x,y = self.startCoord
            self.fill_rect(x, y, self.block , self.block , "#0F0")

        if self.finishCoord:
            x,y = self.finishCoord
            self.fill_rect(x, y, self.block , self.block , "#F00")

    """
    Event handlers for the mouse down event.
    Alt + LeftClick = add obstacle
    Ctrl + LeftClick = place start location
    Command + LeftClick = place end location
    Shift + LeftClick = Draw a line obstacle
    """
    def on_mouse_down(self,e):
        print e
        #Alt key gets you bigger blocks
        x,y = self.adjustCoords(e.x,e.y)

        if not e.alt_key and not e.ctrl_key and not e.meta_key:
            self.toggleObstacle(x,y)

        if e.alt_key:
            pass
        elif e.ctrl_key:
            self.addStart(x,y)
        elif e.meta_key:
            self.addFinish(x,y)
        elif e.shift_key:
            self.drawLine(x,y)

    """
    Key press handlers
    """
    def on_key_down(self,e):
        print e
        if e.key_code==32: # S key
            self.refreshWorld()
        if e.key_code==83: # S key
            pass
        elif e.key_code==70: # F key
            pass

    """
    This simply draws a complete line on the x axis (minus 1 cell).
    """
    def drawLine(self,x,y):
        for i in range(0,self.width,self.block):
            print i,y
            self.toggleObstacle(i,y)

    """
    Double Click starts the path finding.
    """
    def on_dbl_click(self,e):
        print e
        self.startAstar()



    """
    Space bar erases the path, so you can go again
    """
    def refreshWorld(self):
        self.pathFound = False
        self.path = []

    """
    Adds the start cell
    """
    def addStart(self,x,y):
        self.fill_rect(x, y, self.block , self.block , "#F00")
        self.startCoord =(x,y)

    """
    Adds the finish cell
    """
    def addFinish(self,x,y):
        self.fill_rect(x, y, self.block , self.block , "#0F0")
        self.finishCoord = (x,y)

    """
    Fattens the coords to fit grid.
    """
    def adjustCoords(self,x,y):
        """adjust the coords to fit our grid"""
        x = (x / self.block) * self.block
        y = (y / self.block) * self.block
        return (x,y)
"""
Main Driver!!!
"""
if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(DrawAstar)
    app.run()
