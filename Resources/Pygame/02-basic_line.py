import pygame
import random 

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (800, 600)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

points = [(0,0),(random.randrange(0,width),random.randrange(0,height)),(width,height)]

"""
  - add static points
  - add random points
  - show event loop 
  - refresh rate
"""
    
running = True
while running:
  pygame.draw.lines(screen, black, False, points, 2)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  pygame.display.flip()