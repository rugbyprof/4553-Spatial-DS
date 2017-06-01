import pantograph
import math
import random

class MyStuff(pantograph.PantographHandler):
    
    def setup(self):
        self.numBalls = 500

        self.balls = []
        self.createBalls()
        print(self.balls)
        
    def createBalls(self):
        for i in range(self.numBalls):
            self.balls.append([random.uniform(1, self.width),random.uniform(1,self.height),"#%06x" % random.randint(0, 0xFFFFFF)])
    
    def moveBalls(self):
        for i in range(self.numBalls):
            negate = random.randint(0,311) % 2
            if negate == 0:
                negate = -1
            else:
                negate = 1
            d1 = random.randint(1, 1) * random.randint(1, 1) * negate
            d2 = random.randint(1, 1) * random.randint(1, 1) * negate
            self.balls[i][0] += d1
            self.balls[i][1] += d2
            
    def drawBalls(self):
         for i in range(self.numBalls):
            self.fill_circle(self.balls[i][0], self.balls[i][1], 10, color = self.balls[i][2])       

    def update(self):
        self.moveBalls()
        self.clear_rect(0, 0, self.width, self.height)
        self.drawBalls()
        
        
if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(MyStuff)
    app.run()
