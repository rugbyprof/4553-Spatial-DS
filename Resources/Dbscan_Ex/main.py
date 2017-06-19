import pygame
import random
from dbscan import *
import sys,os
import pprint as pp
import json


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs) 
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """
    for id in range(len(clusters)-1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs


def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (600, 400)

# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption('Simple Line')
# screen.fill(background_colour)

# pygame.display.flip()

epsilon = 20
min_pts = 5.0

points = []

num_points = 500

for i in range(num_points):
    x = random.randint(10,width-10)
    y = random.randint(10,height-10)
    points.append((x,y))

# mbrs = calculate_mbrs(points, epsilon, min_pts)

# f = open('F:\\4553-Spatial-DS\\Resources\\Dbscan_Ex\\mbrs.json','w')
# f.write(json.dumps(mbrs))
# f.close()

f = open('F:\\4553-Spatial-DS\\Resources\\Dbscan_Ex\\mbrs.json','r')
data = json.loads(f.read())
print(len(data))

# running = True
# while running:

#     for p in points:
#         pygame.draw.circle(screen, black, p, 3, 0)
#     for mbr in mbrs:
#         pygame.draw.polygon(screen, black, mbr, 2)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             clean_area(screen,(0,0),width,height,(255,255,255))
#             points.append(event.pos)
#             mbrs = calculate_mbrs(points, epsilon, min_pts)
#     pygame.display.flip()