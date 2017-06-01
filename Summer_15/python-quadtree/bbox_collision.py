
import random
import pantograph

from quadtree import QuadTree, RectData


def draw_quadtree(surface, node):
	for n in node.nodes:
		draw_quadtree(surface, n)
		pygame.draw.rect(surface, (192,192,192), pygame.Rect(n.x, n.y, n.w+1, n.h+1), 1)
		for d in n.data:
			pygame.draw.rect(surface, d.data, pygame.Rect(d.x, d.y, d.w, d.h))
	for d in node.data:
		pygame.draw.rect(surface, d.data, pygame.Rect(d.x, d.y, d.w, d.h))

class DrawTree(pantograph.PantographHandler):

    def setup(self):
        self.quadtree = QuadTree(8, self.width, self.height)

        self.buffer = 15

        self.numRectangles = 100
        self.numPoints = 100

        self.rectangles = []
        self.points = []

        self.rectColor = "#354F00"
        self.pointColor = "#567714"
        self.backColor = "#97A084"
        self.collRectColor = "#441154"

        self.maxRectSize = 100
        self.minRectSize = 20

        self.pointSize = 5

        self.collRectWidth = 150
        self.collRectHeight = 150

        self.collRect = RectData(0,0,self.collRectWidth,self.collRectHeight,"#F00")

        for i in range(self.numRectangles):
            vals = self.genRandomVals("rectangle")
            rect = RectData(vals.x, vals.y, vals.w, vals.h, self.rectColor)
            self.rectangles.append(rect)
            self.quadtree.add(rect)

        for i in range(self.numPoints):
            vals = self.genRandomVals("point")
            point = RectData(vals.x, vals.y, vals.w, vals.h, self.pointColor)
            self.points.append(point)
            self.quadtree.add(point)

        self.draw_rect(0, 0, self.width, self.height, "#000")
        self.draw_rect(self.collRect.x,self.collRect.y,self.collRect.w,self.collRect.h,self.collRect.data)



    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        self.drawShapes()
        self.selected = [rect for rect in self.quadtree.querry(self.collRect.x,self.collRect.y,self.collRect.w,self.collRect.h)]
        self.drawSelected()
        self.moveCollRect()


    def drawSelected(self):
        for rect in self.selected:
            self.draw_rect(rect.x, rect.y, rect.w, rect.h, "#FFA500")

    def moveCollRect(self):
        self.collRect.x += 5

        if self.collRect.x >= self.width:
            self.collRect.x = 0
            self.collRect.y = (self.collRect.y + self.collRectHeight) % self.height


    def drawShapes(self):
        for rect in self.rectangles:
            self.draw_rect(rect.x, rect.y, rect.w, rect.h, rect.data)

        for point in self.points:
            self.fill_rect(point.x, point.y, point.w, point.h, point.data)

        self.draw_rect(0, 0, self.width, self.height, "#000")
        self.draw_rect(self.collRect.x,self.collRect.y,self.collRect.w,self.collRect.h,self.collRect.data)


    def genRandomVals(self,shape="rectangle"):
        x = random.randint(0,self.width-(self.buffer*2))
        y = random.randint(0,self.height-(self.buffer*2))
        h = random.randint(self.minRectSize,self.maxRectSize)
        w = random.randint(self.minRectSize,self.maxRectSize)

        if (y+h) > self.height:
            h = (self.height-self.buffer)

        if (x+w) > self.width:
            w = (self.width-self.buffer)

        if shape == "point":
            h = self.pointSize
            w = self.pointSize

        return Size(x,y,w,h)

    def on_mouse_down(self,InputEvent):
        self.collRect.x = InputEvent.x
        self.collRect.y = InputEvent.y

    def on_mouse_move(self,InputEvent):
        self.collRect.x = InputEvent.x
        self.collRect.y = InputEvent.y


class Size(object):
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(DrawTree)
    app.run()
