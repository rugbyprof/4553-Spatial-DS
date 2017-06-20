# drawCircleArcExample.py     P. Conrad for CS5nm, 10/31/2008
#  How to draw an arc in Pygame that is part of a circle

import pygame
from pygame.locals import *
from sys import exit

import math

pygame.init()
screen = pygame.display.set_mode((640,480))

# We need this if we want to be able to specify our
#  arc in degrees instead of radians

def degreesToRadians(deg):
    return deg/180.0 * math.pi


# Draw an arc that is a portion of a circle.
# We pass in screen and color,
# followed by a tuple (x,y) that is the center of the circle, and the radius.
# Next comes the start and ending angle on the "unit circle" (0 to 360)
#  of the circle we want to draw, and finally the thickness in pixels

def drawCircleArc(screen,color,center,radius,startDeg,endDeg,thickness):
    (x,y) = center
    rect = (x-radius,y-radius,radius*2,radius*2)
    startRad = degreesToRadians(startDeg)
    endRad = degreesToRadians(endDeg)
   
    pygame.draw.arc(screen,color,rect,startRad,endRad,thickness)
    

white = (255,255,255);
red = (255,0,0);
green = (0,255,0);
blue = (0,0,255);

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit();


    screen.fill(white);

    # Part of a red circle, arc from 0 to 90 degrees
    # Center is at 100,100, and radius is 50
    drawCircleArc(screen,red,(100,100),50,0,90,1)

    # Part of a blue circle, arc from 135 to 180 degrees
    # Center is at 200,300, radius is 125, thickness is 2
    drawCircleArc(screen,green,(200,300),125,135,180,2)

    
    # Part of a green circle, arc from -45 to +45 degrees
    # Center is at 300,150, radius is 100, thickness is 3
    drawCircleArc(screen,blue,(300,150),100,-45,+45,3)



    pygame.display.update()

    