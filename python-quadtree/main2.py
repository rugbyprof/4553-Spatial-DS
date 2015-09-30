
import random
import pantograph
import collections

from quadtree import QuadTree, RectData

rects = []


class DrawTree(pantograph.PantographHandler):

    def setup(self):
        self.quadtree = QuadTree(8, self.width, self.height)

        self.buffer = 15

        self.numPoints = 150

        self.points = []

        self.rectColor = "#354F00"
        self.pointColor = "#567714"
        self.backColor = "#97A084"

        self.pointSize = 5

        for i in range(self.numPoints):
            vals = self.genRandomVals()
            point = RectData(vals.x, vals.y, vals.w, vals.h, self.pointColor)
            self.points.append(point)
            self.quadtree.add(point)

        self.draw_rect(0, 0, self.width, self.height, "#000")

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        for p in self.points:
            self.draw_rect(p.x,p.y,p.w,p.h,p.data)
            #self.selected = [rect for rect in self.quadtree.querry(self.collRect.x,self.collRect.y,self.collRect.w,self.collRect.h)]
        self.draw_rect(0, 0, self.width, self.height, "#000")
        self.checkCollisions()


    def checkCollisions(self):
        for p in self.points:
            collisions = [rect for rect in self.quadtree.querry(p.x,p.y,p.w,p.h)]
            for c in collisions:
                self.fill_rect(p.x,p.y,p.w,p.h,"#F00")



    def genRandomVals(self,shape="rectangle"):
        x = random.randint(0,self.width-(self.buffer*2))
        y = random.randint(0,self.height-(self.buffer*2))
        h = self.pointSize
        w = self.pointSize

        return Size(x,y,w,h)


class Size(object):
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h




if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(DrawTree)
    app.run()
