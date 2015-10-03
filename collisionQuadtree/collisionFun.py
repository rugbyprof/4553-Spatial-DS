import math
import random
import numpy as np
from QuadTree import QuadTree

# Add ShapeModules (which holds Point,Rect,Polygon) folder to the path
# so we can use those shapes.
import sys
sys.path.append("../ShapeModules")
from Point import Point
from Rectangle import Rectangle
from Polygon import Polygon
from graphics import *

class Rock(object):
    def __init__(self,size,start,speed,dest,wallX,wallY):
        self.start = start
        self.current = start
        self.speed = math.sqrt(speed)
        self.dest = dest
        self._calc_vector()
        self.size = size
        self.wallX = wallX
        self.wallY = wallY
        self.winObj = Circle(Point(self.start.x,self.start.y),self.size)

    def _calc_vector(self):
        self.distance = [self.start.x - self.dest.x, self.start.y - self.dest.y]
        self.norm = math.sqrt(self.distance[0]**2 + self.distance[1]**2)
        self.direction = [self.distance[0]/self.norm , self.distance[1]/self.norm ]
        self.vector = [self.direction[0]*self.speed, self.direction[1]*self.speed]

    def new_dest(self,dest):
        self.dest = dest
        self._calc_vector()

    def set_size(self,size):
        self.size = size

    def move_rock(self):

        if (self.current.x + self.vector[0]) >= self.wallX or (self.current.x + self.vector[0]) <= 0 :
            self.vector[0] *= -1

        if (self.current.y + self.vector[1]) >= self.wallY or (self.current.y + self.vector[1]) <= 0:
            self.vector[1] *= -1

        self.current.x += self.vector[0]
        self.current.y += self.vector[1]
        self.winObj()


class driver(object):
    def __init__(self,win,width,height):
        self.win = win
        self.height = height
        self.width = width
        self.rockSize = 7
        self.rocks = []
        self.rockSpeeds = np.arange(1,15,1)
        self.numRocks = 100

        xWalls = [0,self.width]
        yWalls = [0,self.height]

        for i in range(self.numRocks):
            startX = random.randint(0+self.rockSize,int(self.width)-self.rockSize)
            startY = random.randint(0+self.rockSize,int(self.height)-self.rockSize)

            destX = random.choice(xWalls)
            destY = random.choice(yWalls)

            speed = random.choice(self.rockSpeeds)

            r = Rock(self.rockSize,Point(startX,startY),speed,Point(destX,destY),self.width,self.height)
            self.rocks.append(r)
            r.winObj.draw(self.win)


        self.win.getMouse() # Pause to view result
        self.win.close()    # Close window when done
        #self.drawShapes()

    def drange(self,start, stop, step):
        r = start
        while r < stop:
            yield r
            r += step

    def moveShapes(self):
        for r in self.rocks:
            r.move_rock()


    def drawShapes(self):
        for r in self.rocks:
            self.fill_oval(r.current.x, r.current.y, r.size, r.size,"#F00")


    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        # draw the circle for the "rim" of the wheel
        self.drawShapes()
        self.moveShapes()


if __name__ == '__main__':
    width = 1000
    height = 1000
    win = GraphWin("Collision Fun", width, height)
    driver(win,width,height)
