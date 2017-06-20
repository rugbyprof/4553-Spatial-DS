import pygame
import random 

background_colour = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

(width, height) = (800, 600)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

"""
wont run as is ...
"""


pygame.draw.lines(screen, color, closed, pointlist, thickness)
"""draws a series of lines, connecting the points specified in pointlist
pointlist is a list of tuples, specifying a series of points, e.g. to draw a V you might use [(100,100), (150,200), (200,100)], with closed = False
closed should be either True or False, indicating whether to connect the last point back to the first
thickness is the thickness of the line (in pixels).
Example: pygame.draw.lines(screen, black, False, [(100,100), (150,200), (200,100)], 1)
"""

pygame.draw.rect(screen, color, (x,y,width,height), thickness)
"""draws a rectangle
(x,y,width,height) is a Python tuple
x,y are the coordinates of the upper left hand corner
width, height are the width and height of the rectangle
thickness is the thickness of the line. If it is zero, the rectangle is filled
pygame.draw.circle(screen, color, (x,y), radius, thickness)
draws a circle
(x,y) is a Python tuple for the center, radius is the radius
thickness is the thickness of the line. If it is zero, the rectangle is filled
"""

running = True
while running:
  drawLine(screen)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  pygame.display.flip()