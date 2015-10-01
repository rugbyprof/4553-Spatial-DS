import pantograph
import math
import random
import numpy as np

# Add ShapeModules (which holds Point,Rect,Polygon) folder to the path
# so we can use those shapes.
import sys
sys.path.append("../ShapeModules")
from Point import Point
from Rectangle import Rectangle
from Polygon import Polygon

class Rock(object):
    def __init__(self,size,start,speed,dest,maxX,maxY):
        self.start = start
        self.current = start
        self.speed = math.sqrt(speed)
        self.dest = dest
        self._calc_vector()
        self.size = size
        self.maxX = maxX
        self.maxY = maxY


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

        if (self.current.x + self.vector[0]) >= self.maxX or (self.current.x + self.vector[0]) <= 0 :
            self.vector[0] *= -1

        if (self.current.y + self.vector[1]) >= self.maxY or (self.current.y + self.vector[1]) <= 0:
            self.vector[1] *= -1

        self.current.x += self.vector[0]
        self.current.y += self.vector[1]


class collisionDetection(pantograph.PantographHandler):
    def setup(self):
        self.rockSize = 7
        self.rocks = []
        self.rockSpeeds = np.arange(1,15,1)
        self.numRocks = 100

        seqX = [0,self.width]
        seqY = [0,self.height]

        for i in range(self.numRocks):
            startX = random.randint(int(self.width/4),int(self.width/2))
            startY = random.randint(int(self.width/4),int(self.height/2))

            destX = random.choice(seqX)
            destY = random.choice(seqY)
            speed = random.choice(self.rockSpeeds)

            self.rocks.append(Rock(self.rockSize,Point(startX,startY),speed,Point(destX,destY),self.width,self.height))

        self.drawShapes()

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
    app = pantograph.SimplePantographApplication(collisionDetection)
    app.run()
