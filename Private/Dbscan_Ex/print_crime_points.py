import pygame
import random
from dbscan import *
import sys,os
import pprint as pp
import math
import glob

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

    for id,cpoints in clusters.items():
        if id == '-1':
            continue
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
    


class crime_data(object):
    def __init__(self,file_name):
        self.file_name = file_name
        self.keys = []
        self.data = []
        self.loc_data = {'points':[],'extremes':[]}
        self.xvals = []
        self.yvals = []
        self.latvals = []
        self.lonvals = []
        self.key_words = {}

        self._process_data_file()
        self._calulate_extremes()
        self._adjust_location_coords()


    def _adjust_location_coords(self):
        # xy = self.loc_data['extremes']['xy']
        # deltax = float(xy['maxx']) - float(xy['minx'])
        # deltay = float(xy['maxy']) - float(xy['miny'])
        # maxx = float(xy['maxx'])
        # maxy = float(xy['maxy'])
        # minx = float(xy['minx'])
        # miny = float(xy['miny'])
        maxx = float(1067226)
        maxy = float(271820)
        minx = float(913357)
        miny = float(121250)
        deltax = float(maxx) - float(minx)
        deltay = float(maxy) - float(miny)

        for p in self.loc_data['points']:
            x,y = p['xy']
            x = float(x)
            y = float(y)
            xprime = (x - minx) / deltax
            yprime = ((y - miny) / deltay)
            p['adjusted'] = (xprime,yprime)

    def _process_data_file(self):
        got_keys = False
        with open(self.file_name) as f:
            for line in f:
                # fix line by replacing commas in between double quotes with colons
                line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
                # turn line into a list
                line = line.strip().split(',')
                if not got_keys:
                    self.keys = line
                    got_keys = True
                    continue
                self.data.append(line)
                self._process_location_coords(line)

    def _process_location_coords(self,row):

        x = row[19]                 # get x val from list
        y = row[20]                 # get y val from list
        lat = row[21]               # get lat / lon from list
        lon = row[22]

        if x and y:
            x = int(x)
            y = int(y)
            self.xvals.append(x)
            self.yvals.append(y)

        if lat and lon:
            lat = float(lat)
            lon = float(lon)
            self.latvals.append(lat)
            self.lonvals.append(lon)    

        if lat and lon and x and y:
            self.loc_data['points'].append({'xy':(x,y),'latlon':(lat,lon)})

    def _calulate_extremes(self):
        self.loc_data['extremes'] = {'xy':{'maxx':max(self.xvals),'maxy':max(self.yvals),'minx':min(self.xvals),'miny':min(self.yvals)},
                        'latlon':{'maxlon':max(self.lonvals),'maxlat':max(self.latvals),'minlon':min(self.lonvals),'minlat':min(self.latvals)}}
    

    def get_location_coords(self):
        return self.loc_data

    def get_adjusted_coords(self,width,height):
        adj = []
        i = 0
        for p in self.loc_data['points']:
            x,y = p['adjusted']
            y = 1 - y
            adj.append((int(x*width),int(y*height)))
            i += 1
        return adj

def count_neighbors(points,eps):
    avg_nbrs = {}
    for i in range(len(points)):
        print(i)
        avg_nbrs[i] = 0
        for j in range(len(points)):
            d = distance(points[i],points[j])
            if d == 0:
                continue
            if d < eps:
                avg_nbrs[i] += 1
    return avg_nbrs 

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

class FileHelper(object):
    def __init__(self,directory):
        self.directory = directory
        self.data_by_borough = glob.glob(self.directory+'data_by_borough/*.csv')
        self.data_by_crime = glob.glob(self.directory+'data_by_crime/*.csv')

    def get_data(self,borough=None,crime=None):
        data = []

        assert borough is not None or crime is not None

        if borough is not None:
            assert borough.lower() in ['bronx','manhattan','queens','brooklyn','staten_island']
        if crime is not None:
            assert crime.lower() in ['larceny','assault','drugs','fraud','harrassment']

        if borough is not None:
            for file in self.data_by_borough:
                if borough.lower() in file.lower():
                    data.extend(self._read_file(file,crime))
        elif crime is not None:
            for file in self.data_by_crime:
                if crime.lower() in file.lower():
                    data.extend(self._read_file(file,borough))
        else:
            return []

        return data
    
    def _read_file(self,filename,key):
        data = []
        with open(filename) as f:
            for line in f:
                line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
                if key is not None:
                    if key.lower() in line.lower():
                        data.append(line.strip().split(','))
                else:
                    data.append(line.strip().split(','))
        return data


fh = FileHelper('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/')
data = fh.get_data(borough='manhattan',crime='larceny')
#print(data)
print(len(data))
sys.exit()


data_folder = "/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/"

#cd = crime_data(DIRPATH+'/'+'Nypd_Crime_01')
cd1 = crime_data('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/all_crimes_by_burough/bronx.csv')
cd2 = crime_data('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/all_crimes_by_burough/brooklyn.csv')
cd3 = crime_data('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/all_crimes_by_burough/manhattan.csv')
cd4 = crime_data('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/all_crimes_by_burough/queens.csv')
cd5 = crime_data('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/all_crimes_by_burough/staten_island.csv')


background_colour = (255,255,255)
black = (0,0,0)
width,height = (1000,1000)

points1 = cd1.get_adjusted_coords(width,height)
points2 = cd2.get_adjusted_coords(width,height)
points3 = cd3.get_adjusted_coords(width,height)
points4 = cd4.get_adjusted_coords(width,height)
points5 = cd5.get_adjusted_coords(width,height)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dbscan Example')
screen.fill(background_colour)

pygame.display.flip()

# epsilon = 5
# min_pts = 5.0

# avgnbs = count_neighbors(points1,5)
# print(avgnbs)


#mbrs1 = calculate_mbrs(points1, epsilon, min_pts)

#del mbrs[-1]

running = True
while running:

    for p1 in points1:
        pygame.draw.circle(screen, (2,120,120), p1, 1, 0)
    for p2 in points2:
        pygame.draw.circle(screen, (194,35,38), p2, 1, 0)
    for p3 in points3:
        pygame.draw.circle(screen, (243,115,56), p3, 1, 0)
    for p4 in points4:
        pygame.draw.circle(screen, (128,22,56), p4, 1, 0)
    for p5 in points5:
        pygame.draw.circle(screen, (253,182,50), p5, 1, 0)

    # for mbr in mbrs:
    #     pygame.draw.polygon(screen, black, mbr, 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen,DIRPATH+'/'+'screen_shot.png')
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clean_area(screen,(0,0),width,height,(255,255,255))
            # points.append(event.pos)
            # mbrs = calculate_mbrs(points, epsilon, min_pts)
    pygame.display.flip()