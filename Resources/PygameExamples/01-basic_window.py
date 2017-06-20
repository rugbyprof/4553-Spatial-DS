# import the pygame library
import pygame

# set a backround color with (red,green,blue) RGB color (more later)
background_colour = (255,255,255)

# width and height of window
(width, height) = (300, 200)

# set var (screen) that our 'instance' of the game object
screen = pygame.display.set_mode((width, height))

# set the window 'name' 
pygame.display.set_caption('Basic Window')

# background color of window
screen.fill(background_colour)

# render window
pygame.display.flip()

# setup game loop
running = True

# while 'True', loop
while running:

    # loop throught set of events (probably won't discuss)
    for event in pygame.event.get():
        
        # if red 'X' clicked, kill window
        if event.type == pygame.QUIT:
            running = False