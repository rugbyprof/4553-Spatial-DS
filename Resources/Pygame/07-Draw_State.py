import json
import os 
import pygame
import random 

class colors(object):
    def __init__(self,file_name):
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_rgb(self,name):
        for c in self.content:
            if c['name'] == name:
                return (c['rgb'][0],c['rgb'][1],c['rgb'][2])
        return None

class us_states(object):
    def __init__(self,file_name):
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_state_polygon(self,name):
        for s in self.content:
            if s['name'] == name:
                t = []
                for poly in s['borders']:
                    np = []
                    for p in poly:
                        np.append((p[0],p[1]))
                    t.append(np)
                return(t)
                
        return None


dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = dir_path + '/../Json_Files/colors.json'
c = colors(file_name)

file_name = dir_path + '/../Json_Files/state_borders.json'
s = us_states(file_name)


background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (800, 600)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

poly = s.get_state_polygon('Delaware')

print(poly)

running = True
while running:
    for p in poly:
        pygame.draw.lines(screen, black, False, p, 2)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        pygame.display.flip()