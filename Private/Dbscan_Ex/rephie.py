#Rephael Edwards
#Assignment 2
import pygame
import random
from dbscan import *
import sys,os
import pprint as pp

color_options = {}
keys = []
crimes = []
bronx_crimes = []
#get working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

def create_list():
    got_keys = False
    with open('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/data_by_crime/Assault_Bronx.csv') as f:
        for line in f:
            line = line.strip().split(',')
            if not got_keys:
                keys = line
                #print(keys)
                got_keys = True
                continue

            crimes.append(line)
    for crime in crimes:
        if crime[19] != "" and crime[20] != "":
            bronx_crimes.append((int(crime[19]),int(crime[20])))    
    return bronx_crimes
    

def assign_colors():
    yellow = (255,255,0)
    blue = (0,0,255)
    green = (0,255,0)
    red = (255,0,0)
    purple = (102,0,204)
    self.color_options = {'BRONX':'yellow', 'BROOKLYN':'blue', 'MANHATTAN':'green', 'QUEENS':'red', 'STATEN ISLAND':'purple'}

def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    print("in loop")
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
(width, height) = (1000, 1000)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Crime Clusters')
screen.fill(background_colour)
pygame.display.flip()


epsilon = 20
min_pts = 5.0

points = []
scaled_points = []
xlist = []
ylist = []
newxlist = []
newylist = []
num_points = 1000
intxlist = []
intylist = []


# for i in range(num_points):
#     x = random.randint(10,width-10)
#     y = random.randint(10,height-10)

bronx_crimes = create_list()
for item in bronx_crimes:
    x = item[0]
    y = item[1]
    xlist.append(x)
    ylist.append(y)
# intxlist = [int(p) for p in xlist] 
# intylist = [int(z) for z in ylist]
maxX = max(xlist)
minX = min(xlist)
print(minX)
# i = 0
# for item in xlist:
#     if item < "0":
#         print(i)
#     i = i+1
maxY = max(ylist)
minY = min(ylist)

for x in xlist:
    newx = ((float(x) - float(minX)) / (float(maxX) - float(minX))) * 1000.0
    newxlist.append(newx)
for y in ylist:
    newy = (1 - ((float(y) - float(minY)) / (float(maxY) - float(minY)))) * 1000.0
    newylist.append(newy)  
for r in range(len(bronx_crimes)-1):
    scaled_points.append((int(newxlist[r]),int(newylist[r])))
    print(scaled_points)
print("no")
mbrs = calculate_mbrs(scaled_points, epsilon, min_pts)
print("yes")


# running = True
# while running:
#     for p in scaled_points:
#         pygame.draw.circle(screen, black, p, 3, 0)
#     for mbr in mbrs:
#         pygame.draw.polygon(screen, black, mbr, 2)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             clean_area(screen,(0,0),width,height,(255,255,255))
#             scaled_points.append(event.pos)
#             mbrs = calculate_mbrs(scaled_points, epsilon, min_pts)
#     pygame.display.flip()