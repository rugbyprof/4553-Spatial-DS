import json
import os,sys
import pygame
import random 
import math

DIRPATH = os.path.dirname(os.path.realpath(__file__))

#####################################################################################
#####################################################################################

class Colors(object):
    """
    Opens a json file of web colors.
    """
    def __init__(self,file_name):
        
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_random_color(self):
        r = random.randint(0,len(self.content)-1)
        c = self.content[r]
        return (c['rgb'][0],c['rgb'][1],c['rgb'][2])

    def get_rgb(self,name):
        for c in self.content:
            if c['name'] == name:
                return (c['rgb'][0],c['rgb'][1],c['rgb'][2])
        return None

    def __getitem__(self,color_name):
        """
        Overloads "[]" brackets for instance
        """
        return self.get_rgb(color_name)

#####################################################################################
#####################################################################################

class us_states(object):
    """
    Opens a json file of the united states borders for each state.
    """
    def __init__(self,file_name):
        """
        Args:
            filename (string) : The path and filename to open
        Returns:
            None
        """
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_state_polygon(self,name):
        """
        Returns a polygon of a single state from the US.
        Args:
            name (string): Name of a single state. 

        Returns:
            json (string object): Json representation of a state
        """
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

    def get_continental_states(self):
        """
        Returns a polygon of all the continental us states.
        Args:
            None

        Returns:
            json (string object): Json representation of each continental state
        """
        states = []
        for s in self.content:
            t = []
            if s['name'] not in ['Alaska','Hawaii']:
                for poly in s['borders']:
                    np = []
                    for p in poly:
                        np.append((p[0],p[1]))
                    t.append(np)
                states.append(t)
        return(states)

#####################################################################################
#####################################################################################

class WorldCountries(object):
    """
    Opens a json file of the united states borders for each state.
    """
    def __init__(self,file_name):
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)
    
    def get_all_countries(self):
        all_countries = []
        for c in self.content['features']:
            if c['id'] in ["ATA"]:
                continue
            all_countries.append(c['geometry']['coordinates'])
        return all_countries

    def get_country(self,id):
        country = []
        for c in self.content['features']:
            if c['id'] == id:
                country.append(c['geometry']['coordinates'])
        return country  
            

#####################################################################################
#####################################################################################

class DrawGeoJson(object):
    def __init__(self,screen,width,height):
        """
        Converts lists (polygons) of lat/lon pairs into pixel coordinates in order to do some 
        simple drawing using pygame. 
        """
        self.screen = screen    # window handle for pygame drawing

        self.polygons = []      # list of lists (polygons) to be drawn

        self.all_lats = []      # list for all lats so we can find mins and max's
        self.all_lons = []

        self.mapWidth = width       # width of the map in pixels
        self.mapHeight = height     # height of the map in pixels
        self.mapLonLeft = -180.0    # extreme left longitude
        self.mapLonRight = 180.0    # extreme right longitude
        self.mapLonDelta = self.mapLonRight - self.mapLonLeft # difference in longitudes
        self.mapLatBottom = 0.0     # extreme bottom latitude
        self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0 # bottom in degrees

        self.colors = Colors(DIRPATH + '/../Json_Files/colors.json')

    def convertGeoToPixel(self,lon, lat):
        """
        Converts lat/lon to pixel within a set bounding box
        Args:
            lon (float): longitude
            lat (float): latitude

        Returns:
            point (tuple): x,y coords adjusted to fit on print window
        """
        x = (lon - self.mapLonLeft) * (self.mapWidth / self.mapLonDelta)

        lat = lat * math.pi / 180.0
        self.worldMapWidth = ((self.mapWidth / self.mapLonDelta) * 360) / (2 * math.pi)
        self.mapOffsetY = (self.worldMapWidth / 2 * math.log((1 + math.sin(self.mapLatBottomDegree)) / (1 - math.sin(self.mapLatBottomDegree))))
        y = self.mapHeight - ((self.worldMapWidth / 2 * math.log((1 + math.sin(lat)) / (1 - math.sin(lat)))) - self.mapOffsetY)

        return (x, y)


    def add_polygon(self,poly):
        """
        Add a polygon to local collection to be drawn
        Args:
            poly (list): list of lat/lons

        Returns:
            None
        """
        self.polygons.append(poly)
        for p in poly:
            x,y = p
            self.all_lons.append(x)
            self.all_lats.append(y)
        self.__update_bounds()


    def draw_polygons(self):
        """
        Draw our polygons to the screen
        Args:
            None

        Returns:
            None
        """ 
        black = (0,0,0)
        for poly in self.polygons:
            adjusted = []
            for p in poly:
                x,y = p
                adjusted.append(self.convertGeoToPixel(x,y))
            pygame.draw.lines(self.screen, self.colors.get_random_color(), False, adjusted, 1)

    def __update_bounds(self):
        """
        Updates the "extremes" of all the points added to be drawn so
        the conversion to x,y coords will be adjusted correctly to fit
        the "bounding box" surrounding all the points. Not perfect.
        Args:
            None

        Returns:
            None
        """  
        self.mapLonLeft = min(self.all_lons)
        self.mapLonRight = max(self.all_lons)
        self.mapLonDelta = self.mapLonRight - self.mapLonLeft  
        self.mapLatBottom = min(self.all_lats)
        self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0


    def __str__(self):
        return "[%d,%d,%d,%d,%d,%d,%d]" % (self.mapWidth,self.mapHeight,self.mapLonLeft,self.mapLonRight,self.mapLonDelta,self.mapLatBottom,self.mapLatBottomDegree)


#####################################################################################
#####################################################################################

def point_in_poly(self,x,y,poly):
    """
    Determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs. This function
    returns True or False.  The algorithm is called
    the "Ray Casting Method".
    """
    x = self.lon2canvas(x)
    y = self.lat2canvas(y)
    poly = self.poly2canvas(poly)
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

#####################################################################################
#####################################################################################

def mercator_projection(latlng,zoom=0,tile_size=256):
    """
    The mapping between latitude, longitude and pixels is defined by the web
    mercator projection.
    """
    x = (latlng[0] + 180) / 360 * tile_size
    y = ((1 - math.log(math.tan(latlng[1] * math.pi / 180) + 1 / math.cos(latlng[1] * math.pi / 180)) / math.pi) / 2 * pow(2, 0)) * tile_size
   
    return (x,y)

if __name__ == '__main__':

    zoom_level = 0

    width = 1024
    height = 512

    file_name = DIRPATH + '/../Json_Files/state_borders.json'
    s = us_states(file_name)

    file_name = DIRPATH + '/../Json_Files/countries.geo.json'

    w = WorldCountries(file_name)

    background_colour = (255,255,255)
    black = (0,0,0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Draw Stuff')
    screen.fill(background_colour)

    pygame.display.flip()

    gd = DrawGeoJson(screen,width,height)

    states = []
    countries = []


    countries = w.get_all_countries()

    raw_states = s.get_continental_states()

    for state_polys in raw_states:
        for poly in state_polys:
            gd.add_polygon(poly)

    print(gd)


    # for country_polys in countries:
    #     for poly in country_polys:
    #         print(type(poly[0][0]))
    #         if type(poly[0][0]) is float:
    #             gd.add_polygon(poly)
    #         else:
    #             for sub_poly in poly:
    #                 gd.add_polygon(sub_poly)

    country = w.get_country('FRA')

    for polys in country:
        for poly in polys:
            if type(poly[0][0]) is float:
                gd.add_polygon(poly)
            else:
                for sub_poly in poly:
                    gd.add_polygon(sub_poly)

    country = w.get_country('GRC')
    for polys in country:
        for poly in polys:
            if type(poly[0][0]) is float:
                gd.add_polygon(poly)
            else:
                for sub_poly in poly:
                    gd.add_polygon(sub_poly)

    country = w.get_country('ESP')
    for polys in country:
        for poly in polys:
            if type(poly[0][0]) is float:
                gd.add_polygon(poly)
            else:
                for sub_poly in poly:
                    gd.add_polygon(sub_poly)

    print(gd)

    running = True
    while running:
        gd.draw_polygons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            pygame.display.flip()