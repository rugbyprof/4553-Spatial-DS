import pygame
from rich import print
from point import Point
from ball import Ball
import random
from rectangle import Rectangle
from rectangle import Bounds
from pointQuadTree import PointQuadTree

import sys

# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BUFFER = 20

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

TREE_WIDTH = SCREEN_WIDTH - BUFFER
TREE_HEIGHT = SCREEN_HEIGHT - BUFFER


################################################################################
#  _____ ____  _____ _____ ____  ____  _____     _______ ____
# |_   _|  _ \| ____| ____|  _ \|  _ \|_ _\ \   / / ____|  _ \
#   | | | |_) |  _| |  _| | | | | |_) || | \ \ / /|  _| | |_) |
#   | | |  _ <| |___| |___| |_| |  _ < | |  \ V / | |___|  _ <
#   |_| |_| \_\_____|_____|____/|_| \_\___|  \_/  |_____|_| \_\
################################################################################


class TreeDriver(object):
    def __init__(self, **kwargs):

        self.width = kwargs.get("width", TREE_WIDTH)  # tree bbox width
        self.height = kwargs.get("height", TREE_HEIGHT)  # tree bbox height
        self.primePoints = kwargs.get("primePoints", 0)  # prime tree with N points
        self.loadPoints = kwargs.get("loadPoints", [])  # load a list of points
        self.ballColor = kwargs.get("ballColor", (0, 255, 0))  # generic ball color
        self.ballRadius = kwargs.get("ballRadius", 5)  # generic ball color
        self.ballDx = kwargs.get("dx", 5)  #
        self.ballDy = kwargs.get("dy", 5)  # g

        self.bbox = Rectangle(p1=Point(0, 0), p2=Point(self.width, self.height))
        self.bounds = Bounds(0, 0, self.width, self.height)
        self.tree = PointQuadTree(self.bbox, 1, 0)

        self.pid = 0
        self.balls = []
        self.rects = []

        # if list or number of points passed in, call init function
        if len(self.loadPoints) > 0:
            self.initBalls(self.loadPoints)
        elif self.primePoints > 0:
            self.initBalls(self.primePoints)

    def initBalls(self, balls):
        """Load quadtree with any pre-existing points"""

        # if points == int then we load "points" number of balls into the tree
        if isinstance(balls, int):
            while self.pid < balls:
                x = int(self.width * random.random())
                y = int(self.height * random.random())
                ball = Ball(
                    x,
                    y,
                    data={"id": self.pid},
                    color=self.ballColor,
                    radius=self.ballRadius,
                    dx=self.ballDx,
                    dy=self.ballDy,
                )
                self.tree.insert(ball)
                self.balls.append(ball)
                self.pid += 1

        # else if points is a "list" of points or balls, we handle that as well
        elif isinstance(balls, list):
            for ball in balls:
                if isinstance(ball, Ball):
                    ball.data["id"] = self.pid
                    self.tree.insert(ball)
                    self.balls.append(ball)
                elif isinstance(ball, Point):
                    ball.data["id"] = self.pid
                    ball = Ball(
                        ball.x, ball.y, data=ball.data, dx=self.ballDx, dy=self.ballDy
                    )
                self.tree.insert(ball)
                self.balls.append(ball)
                self.pid += 1

    def moveBalls(self):
        bounds = Bounds(5 + BUFFER // 2, 0 + BUFFER // 2, self.width, self.height)
        for ball in self.balls:
            ball.move(bounds)

    def appendBall(
        self,
        x,
        y,
    ):
        self.balls.append(Ball(x, y, radius=self.ballRadius, color=self.ballColor))

    def getBalls(self):
        return self.balls

    def getRectangles(self):
        return self.tree.getBBoxes()

    def updateTree(self, moveBalls=True):
        if moveBalls:
            self.moveBalls()
        self.tree.reset(self.bbox, self.balls)


################################################################################
#   ____    _    __  __ _____ ____  ____  _____     _______ ____
#  / ___|  / \  |  \/  | ____|  _ \|  _ \|_ _\ \   / / ____|  _ \
# | |  _  / _ \ | |\/| |  _| | | | | |_) || | \ \ / /|  _| | |_) |
# | |_| |/ ___ \| |  | | |___| |_| |  _ < | |  \ V / | |___|  _ <
#  \____/_/   \_\_|  |_|_____|____/|_| \_\___|  \_/  |_____|_| \_\
################################################################################
class GameDriver(object):
    """This would normally be a game class. But, we need a tree handler so
    I'm repurposing a game class I found here:
    http://programarcadegames.com/python_examples/f.php?file=game_class_example.py
    """

    def __init__(self, **kwargs):
        """Init driver class"""

        self.screen = kwargs.get("screen", None)  # screen
        if not self.screen:
            print("Need a pygame screen!")
            sys.exit()

        self.moveBalls = kwargs.get("moveBalls", 1)

        self.treeDriver = TreeDriver(screen=self.screen)

        self.localRects = []

        self.events = {
            "data": {},
            "keysPressed": {},
        }  # pygame events mouse clicks keys etc
        self.pressed = {}  # which keys pressed

    def captureEvents(self):
        """Handles events like mouse clicks and closing game window.
        Returns:
            dictionary :  a dictionary with keys indicating events that happened
        Examples:
            returns a mouse click event
            {
                "mouseUp" : (345,23)
            }
            returns a keyboard or kill window event
            {
                "quit" : True
            }

            As far a keys pressed go, there are other ways to identify keys pressed,
            some that used predefined strings to help with determining what key.
            Examples below at link:
            https://github.com/search?q=pygame.key.get_pressed&type=Code&l=Python
        """

        # loop through events captured by game loop
        for event in pygame.event.get():

            # if we hit escape or click x on window
            if event.type == pygame.QUIT:
                self.events["quit"] = True

            # if a key is pressed down, remember it
            if event.type == pygame.KEYDOWN:

                mods = pygame.key.get_mods()  # modifier keys (ctrl, shift, ...)
                keysPressed = pygame.key.get_pressed()  # list of pressed keys

                # print out keysPressed to see what it returns
                for i in range(len(keysPressed)):
                    if keysPressed[i]:
                        self.events["keysPressed"][i] = True

                # mods contains an integer of last modifier key pressed
                if mods:
                    self.events["keysPressed"][i] = True

                # log which key was pressed (this is not the same as above)
                # just another way to grab pressed keys
                self.events["keydown"] = event.key

            # if a key is released erase everything (but the keys still
            # held down will be instantly placed back in)
            if event.type == pygame.KEYUP:
                self.events["keyup"] = event.key
                self.events["keysPressed"] = {}

            # we pressed a mouse button, maybe released it, maybe not
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.events["mouseDown"] = True
                # 1 == left click
                # 2 == center button
                # 3 = right click

                # if left click
                if event.button == 1:
                    # if "r" is down, we are starting do create a rectangle drag area
                    if 114 in self.events["keysPressed"]:
                        self.events["data"]["clickStart"] = pygame.mouse.get_pos()

            # we released a mouse button
            if event.type == pygame.MOUSEBUTTONUP:
                self.events["mouseUp"] = True
                # 1 == left click
                # 2 == center button
                # 3 = right click

                # if left click
                if event.button == 1:
                    # register click position
                    self.events["data"]["clickPos"] = pygame.mouse.get_pos()

                    # if "r" key is held down, this point is end of rectangle
                    if 114 in self.events["keysPressed"]:
                        self.events["data"]["clickEnd"] = pygame.mouse.get_pos()

            # capture mouse position while its moving
            if event.type == pygame.MOUSEMOTION:
                self.events["data"]["clickMove"] = pygame.mouse.get_pos()

            print(self.events)
        return self.events

    def updateLogic(self, events):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        Params:
            events (dict) : event dictionary created in handleEvents
        """
        if "data" in events:
            if "clickPos" in self.events["data"]:
                x, y = self.events["data"]["clickPos"]
                self.treeDriver.appendBall(x, y)
                del self.events["data"]["clickPos"]

        self.treeDriver.updateTree(self.moveBalls)

        # Move all the balls or sprites

        # check for collision

        # handle collisions or stuff

    def displayFrame(self):
        """Display everything to the screen for the game.
        Params:
            screen (pygame window) : draw stuff to this object
        """
        self.screen.fill(WHITE)

        self.drawBalls()
        self.drawRects()

        pygame.display.flip()

    def gameOver(self):
        """Do stuff like below if your game is over
        Params:
            screen (pygame window) : draw stuff to this object
        """
        # font = pygame.font.Font("Serif", 25)
        font = pygame.font.SysFont("serif", 25)
        text = font.render("Game Over, click to restart", True, BLACK)
        center_x = (TREE_WIDTH // 2) - (text.get_width() // 2)
        center_y = (TREE_HEIGHT // 2) - (text.get_height() // 2)
        self.screen.blit(text, [center_x, center_y])

    def drawBalls(self):
        balls = self.treeDriver.getBalls()
        for ball in balls:
            # print(self.screen, ball.color, [ball.x, ball.y], ball.radius)
            pygame.draw.circle(self.screen, ball.color, [ball.x, ball.y], ball.radius)

    def drawRects(self):
        rectangles = self.treeDriver.getRectangles()
        """left, top, width, height"""
        for rect in rectangles:
            c = rect["color"]
            r = rect["bbox"]
            p = rect["parent"]
            l = r.left + BUFFER // 2
            t = r.top + BUFFER // 2
            w = r.w
            h = r.h

            pygame.draw.rect(self.screen, c, pygame.Rect(l, t, w, h), 1)


def initSomeBalls(bounds=Bounds(0, 0, TREE_WIDTH, TREE_HEIGHT), n=10):
    """Randomly generate some balls to load into the quadtree"""
    balls = []
    for i in range(n):
        x = random.randint(bounds.minX, bounds.maxX)
        y = random.randint(bounds.minY, bounds.maxY)
        balls.append(Ball(x, y, radius=5, color=randomColor()))

    return balls


################################################################################
#  __  __    _    ___ _   _
# |  \/  |  / \  |_ _| \ | |
# | |\/| | / _ \  | ||  \| |
# | |  | |/ ___ \ | || |\  |
# |_|  |_/_/   \_\___|_| \_|
################################################################################


def main():
    """Main program function that does most things pygame"""

    # Initialize Pygame and set up the window
    pygame.init()

    # basic window setup with size and a bounds class
    # for the bouncy balls
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # title the game window, and make the mouse show up
    pygame.display.set_caption("Quadtree Demo")
    pygame.mouse.set_visible(True)

    # Game loop boolean and instance of the pygame clock
    keepLooping = True
    clock = pygame.time.Clock()

    #####################################################################
    # Create an instance of the Game class that drives
    # this whole mess.
    driver = GameDriver(screen=screen, moveBalls=1)

    #####################################################################
    # Main game loop
    while keepLooping:

        # Process events (keystrokes, mouse clicks, etc)
        events = driver.captureEvents()

        # some quit event happened so break out
        if "quit" in events:
            break

        # Update object positions, check for collisions
        driver.updateLogic(events)

        # Draw the current frame
        driver.displayFrame()

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
