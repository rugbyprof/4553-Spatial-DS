import pygame
import random
from dbscan import *
import sys,os


def calculate_mbrs(points, epsilon, min_pts):
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)
    for id,cpoints in clusters.items():
        xs = []
        ys = []
        for p in cpoints:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs

def clean_area(screen,origin,width,height,color):
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (600, 400)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

epsilon = 20
min_pts = 5.0

# points = [(3,16),(3,14),(4,15),(5,14),(5,17),(6,17),(6,16),(6,15),(6,13),
#             (10,6),(10,4),(10,3),(11,4),(12,5),(12,4),(12,3),
#             (18,13),(19,14),(19,13),(19,2),(20,14),(20,13),(20,12),(20,11),(21,13),
#             (23,6),(23,5),(23,4),(23,3),(23,2),(24,5),(24,4),(24,3),(24,2),
#             (10,11),(14,11),(13,16),(19,5),(25,13)]

#points = [(0,0),(random.randrange(0,width),random.randrange(0,height)),(width,height)]

points = []

for i in range(500):
    x = random.randint(10,width-10)
    y = random.randint(10,height-10)
    points.append((x,y))

mbrs = calculate_mbrs(points, epsilon, min_pts)

running = True
while running:
    #pygame.draw.lines(screen, black, False, points, 2)

    for p in points:
        pygame.draw.circle(screen, black, p, 3, 0)
    for mbr in mbrs:
        pygame.draw.polygon(screen, black, mbr, 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clean_area(screen,(0,0),width,height,(255,255,255))
            points.append(event.pos)
            mbrs = calculate_mbrs(points, epsilon, min_pts)
    pygame.display.flip()