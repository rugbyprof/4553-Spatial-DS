import json
import os,sys
import pygame
import random 
import math

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

class mini_map_helper(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def lat2canvas(self,lat):
        """
        Turn a latitude in the form [-90 , 90] to the form [0 , 180]
        """
        return ((float(lat) % 180) / 180) * self.height 

    def lon2canvas(self,lon):
        """
        Turn a longitude in the form [-180 , 180] to the form [0 , 360]
        """
        return ((float(lon) % 360) / 360) * self.width 

    def poly2canvas(self,poly):
        newPoly = []
        for sub_poly in poly:
            new_sub = []
            for p in sub_poly:
                x,y = p
                y = y * -1
                x = self.lon2canvas(x)
                y = self.lat2canvas(y)

                new_sub.append((x,y))
            newPoly.append(new_sub)
        return newPoly

class Point(object):
  def __init__(self,X=0,Y=0):
    self.x = X
    self.y = Y
    
  def __str__(self):
    return "(%s,%s)" % (str(self.x),str(self.y))
    
  def __repr__(self):
    return self.__str__()

  def xy(self):
      return (self.x,self.y)

class LatLng(object):
  def __init__(self,lat=0.0,lng=0.0):
    self.lat = lat
    self.lng = lng
    
  def __str__(self):
    return "(%f,%f)" % (self.lat,self.lng)
  def __repr__(self):
    return self.__str__()

class map_tiles(object):

  def __init__(self,width=1024,height=768):
    self.tile_size = 256
    
  def project_points(self,poly,zoom=8):

    scale = 1 << zoom

    print(scale)
    print(2**zoom*self.tile_size)

    projected_points = []
    for points in poly:
        new_points = []
        for p in points:
            worldCoordinate = self.project(LatLng(p[1],p[0]))
            pixelCoordinate = Point(math.floor(worldCoordinate.x * scale),math.floor(worldCoordinate.y * scale))
            tileCoordinate = Point(math.floor(worldCoordinate.x * scale / self.tile_size),math.floor(worldCoordinate.y * scale / self.tile_size))
            new_points.append(pixelCoordinate.xy())
        projected_points.append(new_points)
    return projected_points
 

  # The mapping between latitude, longitude and pixels is defined by the web
  # mercator projection.
  def project(self,latLng,zoom=8):
    siny = math.sin(latLng.lat * math.pi / 180.0)
  
    # Truncating to 0.9999 effectively limits latitude to 89.189. This is
    # about a third of a tile past the edge of the world tile.
    siny = min(max(siny, -0.9999), 0.9999)
  
    print((0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi)) * 256)

    return Point(self.tile_size * (0.5 + latLng.lng / 360.0), 
                 self.tile_size * (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi)))
  


screen_width = 1024
screen_height = 768

dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = dir_path + '/../Json_Files/colors.json'
c = colors(file_name)

file_name = dir_path + '/../Json_Files/state_borders.json'
s = us_states(file_name)

mh = mini_map_helper(screen_width,screen_height)
mt = map_tiles()

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (screen_width, screen_height)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

states = []
ll = LatLng(lat=-90,lng=0)
print(mt.project(ll,1))
sys.exit()
# print(mt.project(LatLng(lat=90,lng=180),1))
# print(mt.project(LatLng(lat=-90,lng=180),1))
# print(mt.project(LatLng(lat=-90,lng=-180),1))
# print(mt.project(LatLng(lng=-95.690918,lat=40.513798),1))

poly = s.get_state_polygon('Nebraska')
#poly = mh.poly2canvas(poly)
poly = mt.project_points(poly, 8)
print(poly)
for i in range(len(poly)):
    poly[i] = poly[i]
states.append(poly)

# poly = s.get_state_polygon('Florida')
# poly = mh.poly2canvas(poly)
# states.append(poly)

# poly = s.get_state_polygon('Texas')
# poly = mh.poly2canvas(poly)
# states.append(poly)

print(states)

running = True
while running:
    for s in states:
        for p in poly:
            pygame.draw.lines(screen, black, False, p, 2)

    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = False
        pygame.display.flip()