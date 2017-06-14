import json
import os,sys
import pygame
import random
import math

# Get current working path
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
        """
        Returns a random rgb tuple from the color dictionary
        Args:
            None
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            some_color = c.get_random_color()
            # some_color is now a tuple (r,g,b) representing some lucky color
        """
        r = random.randint(0,len(self.content)-1)
        c = self.content[r]
        return (c['rgb'][0],c['rgb'][1],c['rgb'][2])

    def get_rgb(self,name):
        """
        Returns a named rgb tuple from the color dictionary
        Args:
            name (string) : name of color to return
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            lavender = c.get_rgb('lavender')
            # lavender is now a tuple (230,230,250) representing that color
        """
        for c in self.content:
            if c['name'] == name:
                return (c['rgb'][0],c['rgb'][1],c['rgb'][2])
        return None

    def __getitem__(self,color_name):
        """
        Overloads "[]" brackets for this class so we can treat it like a dict.
        Usage:
            c = Colors()
            current_color = c['violet']
            # current_color contains: (238,130,238)
        """
        return self.get_rgb(color_name)

#####################################################################################
#####################################################################################

class StateBorders(object):
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

    def get_state(self,name):
        """
        Returns a polygon of a single state from the US.
        Args:
            name (string): Name of a single state. 

        Returns:
            json (string object): Json representation of a state

        Usage:
            sb = StateBorders()
            texas = sb.get_state_polygon('texas')
            # texas is now a list object containing polygons
        """
        for s in self.content:
            if s['name'].lower() == name.lower() or s['code'].lower() == name.lower():
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
        Returns a list of all the continental us states as polygons.
        Args:
            None

        Returns:
            list (list object): list of Json objects representing each continental state.

        Usage:
            sb = StateBorders()
            states = sb.get_continental_states()
            # states is now a list object containing polygons for all the continental states
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

    def key_exists(self,key):
        """
        Returns boolean if key exists in json
        Args:
            key (string) : some identifier 

        Returns:
            T/F (bool) : True = Key exists
        """
        for s in self.content:
            if s['name'].lower() == key.lower():
                return True
            elif s['code'].lower() == key.lower():
                return True
        return False

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
        """
        Returns a list of all the countries us states.
        Args:
            None

        Returns:
            list (list object): List of Json objects representing each country 

        Usage:
            wc = WorldCountries()
            countries = wc.get_all_countries()
            # countries is now a list object containing polygons for all the countries
        """
        all_countries = []
        for c in self.content['features']:
            if c['id'] in ["ATA"]:
                continue
            all_countries.append(c['geometry']['coordinates'])
        return all_countries

    def get_country(self,id):
        """
        Returns a list of one country.
        Args:
            None

        Returns:
            list (list object): List of Json object representing a country 

        Usage:
            wc = WorldCountries()
            country = wc.get_country('AFG')
            # country is now a list object containing polygons for 'Afghanistan'
        """
        country = []
        for c in self.content['features']:
            if c['id'].lower() == id.lower() or c['properties']['name'].lower() == id.lower():
                country.append(c['geometry']['coordinates'])
        return country  

    def key_exists(self,key):
        """
        Returns boolean if key exists in json
        Args:
            key (string) : some identifier 

        Returns:
            T/F (bool) : True = Key exists
        """
        for c in self.content['features']:
            if c['id'].lower() == key.lower():
                return True
            elif c['properties']['name'].lower() == key.lower():
                return True
        return False
            

#####################################################################################
#####################################################################################

class DrawGeoJson(object):
    __shared_state = {}        
    def __init__(self,screen,width,height):
        """
        Converts lists (polygons) of lat/lon pairs into pixel coordinates in order to do some 
        simple drawing using pygame. 
        """
        self.__dict__ = self.__shared_state

        self.screen = screen    # window handle for pygame drawing

        self.polygons = []      # list of lists (polygons) to be drawn
        self.boxes = []         # list of lists (polygon boxes) to be drawn

        self.all_lats = []      # list for all lats so we can find mins and max's
        self.all_lons = []
        self.box_lats = []
        self.box_lons = []


        self.mapWidth = width       # width of the map in pixels
        self.mapHeight = height     # height of the map in pixels
        self.mapLonLeft = -180.0    # extreme left longitude
        self.boxLonLeft = -180.0
        self.mapLonRight = 180.0    # extreme right longitude
        self.boxLonRight = 180.0
        self.mapLonDelta = self.mapLonRight - self.mapLonLeft # difference in longitudes
        self.boxLonDelta = self.boxLonRight - self.boxLonLeft
        self.mapLatBottom = 0.0     # extreme bottom latitude
        self.boxLatBottom = 0.0
        self.boxLatTop = 0.0
        self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0 # bottom in degrees
        self.boxLatBottomDegree = self.boxLatBottom * math.pi / 180.0

        self.colors = Colors(DIRPATH + '/colors.json')

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



    def add_polygon(self,poly,id=None):
        """
        Add a polygon to local collection to be drawn later
        Args:
            poly (list): list of lat/lons
        Returns:
            None
        """
        self.polygons.append(poly)
        # New added June 13
        if id is not None:
            # if country not in dict, make a list for its polygons
            # to be appended to.
            if id not in self.adjusted_poly_dict:
                self.adjusted_poly_dict[id] = []
            # append poly to dictionary with country as key (id).
            self.adjusted_poly_dict[id].append(poly)   
        for p in poly:
            x,y = p
            self.all_lons.append(x)
            self.all_lats.append(y)
        self.__update_bounds()

    # We should use recursion on these containers with arbitrary depth, but oh well.
    def adjust_poly_dictionary(self):
        #pp.pprint(self.adjusted_poly_dict)
        for country,polys in self.adjusted_poly_dict.items():
            new_polys = []
            print(country)
            for poly in polys:
                new_poly = []
                for p in poly:
                    x,y = p
                    new_poly.append(self.convertGeoToPixel(x,y))
                new_polys.append(new_poly)
            self.adjusted_poly_dict[country] = new_polys
        pp.pprint(self.adjusted_poly_dict)


    def add_box(self,poly):
        """
        Add a polygon to local collection to be drawn later
        Args:
            poly (list): list of lat/lons

        Returns:
            None
        """
        for p in poly:
            x,y = p
            self.box_lons.append(x)
            self.box_lats.append(y)
        poly = self.__update_box_bounds()
        self.boxes.append(poly)

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
            pygame.draw.polygon(self.screen, self.colors.get_random_color(), adjusted, 0)
    
    def draw_boxes(self,box):
        """
        Draw our box to the screen
        Args:
            A list of tuples

        Returns:
            None
        """ 
        black = (0,0,0)
        pygame.draw.polygon(self.screen, black, box, 5)


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

    def __update_box_bounds(self):
        """
        Creates a list of 4 lat,lon points that will be used as a polygon
        which consists of the 4 extreme corners
        Args:
            None

        Returns:
            List of lat,lon to draw polygon box
        """  
        self.boxLonLeft = min(self.box_lons)
        self.boxLonRight = max(self.box_lons)
        self.boxLonDelta = self.boxLonRight - self.boxLonLeft  
        self.boxLatBottom = min(self.box_lats)
        self.boxLatTop = max(self.box_lats)
        self.boxLatBottomDegree = self.boxLatBottom * math.pi / 180.0

        square = []
        square.append((self.boxLatBottom, self.boxLonLeft))
        square.append((self.boxLatTop, self.boxLonLeft))
        square.append((self.boxLatBottom, self.boxLonRight))
        square.append((self.boxLatTop, self.boxLonRight))
        return square

    def make_box(self, box):
        """
        Creates a list of 4 x,y coordinates that will then draw a bounding box
        Args:
            List of Tuples
        Returns
            List of Min/Max Tuples, 4 in total
        """
        BoxTop = -10000000.0
        BoxBottom = 100000000.0
        BoxLeft = -100000000.0
        BoxRight = 100000000.0
        for b in box:
            x,y = b
            if BoxTop <= y:
                BoxTop = y
            if BoxBottom >= y:
                BoxBottom = y
            if BoxLeft <= x:
                BoxLeft = x
            if BoxRight >= x:
                BoxRight = x
        square = []
        square.append((BoxLeft, BoxTop))
        square.append((BoxLeft, BoxBottom))
        square.append((BoxRight, BoxBottom))
        square.append((BoxRight, BoxTop))
        return square


    def __str__(self):
        return "[%d,%d,%d,%d,%d,%d,%d]" % (self.mapWidth,self.mapHeight,self.mapLonLeft,self.mapLonRight,self.mapLonDelta,self.mapLatBottom,self.mapLatBottomDegree)


#####################################################################################
#####################################################################################

class DrawingFacade(object):
    def __init__(self,width,height):
        """
        A facade pattern is used as a type of 'wrapper' to simplify interfacing with one or
        more other classes. This 'facade' lets us interface with the 3 classes instantiated
        below.
        """
        self.sb = StateBorders(DIRPATH + '/state_borders.json')
        self.wc = WorldCountries(DIRPATH + '/countries.geo.json')
        self.gd = DrawGeoJson(screen,width,height)

    def add_polygons(self,ids):
        """
        Adds polygons to the 'DrawGeoJson' class using country names or id's, state names or code's. It
        expects a list of values.
        Args:
            ids (list) : A list of any state or country identifiers

        Returns:
            None

        Usage:
            df.add_polygons(['FRA','TX','ESP','AFG','NY','ME','Kenya'])
        """ 
        for id in ids:
            if self.wc.key_exists(id):
                self.__add_country(self.wc.get_country(id))
            elif self.sb.key_exists(id):
                self.__add_state(self.sb.get_state(id))         

    def __add_country(self,country):
        for polys in country:
            for poly in polys:
                if type(poly[0][0]) is float:
                    gd.add_polygon(poly)
                else:
                    for sub_poly in poly:
                        self.gd.add_polygon(sub_poly)

    def __add_state(self,state):
        for poly in state:
            self.gd.add_polygon(poly)



def point_inside_polygon(x,y,poly):
    """
    determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs.
    http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

#####################################################################################
#####################################################################################

def mercator_projection(latlng,zoom=0,tile_size=256):
    """
    ******NOT USED******
    The mapping between latitude, longitude and pixels is defined by the web mercator projection.
    """
    x = (latlng[0] + 180) / 360 * tile_size
    y = ((1 - math.log(math.tan(latlng[1] * math.pi / 180) + 1 / math.cos(latlng[1] * math.pi / 180)) / math.pi) / 2 * pow(2, 0)) * tile_size
   
    return (x,y)

if __name__ == '__main__':
    pygame.init()

    # if there are no command line args
    if len(sys.argv) == 1:
        width = 1024    # define width and height of screen
        height = 512
    else:
        # use size passed in by user
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    
    # create an instance of pygame
    # "screen" is what will be used as a reference so we can
    # pass it to functions and draw to it.
    screen = pygame.display.set_mode((width, height)) 

    # Set title of window
    pygame.display.set_caption('Draw World Polygons')

    # Set background to white
    screen.fill((255,255,255))

    # Refresh screen
    pygame.display.flip()

    # Instances of our drawing classes
    gd = DrawGeoJson(screen,width,height)
    df = DrawingFacade(width,height)

    # Add countries and states to our drawing facade.
    # df.add_polygons(['FRA','TX','ESP','AFG','NY'])
    # df.add_polygons(['TX','NY','ME','Kenya'])
    df.add_polygons(['Spain','France','Belgium','Italy','Ireland','Scotland','Greece','Germany','Egypt','Morocco','India'])

    print("Matthew Schenk Version 1")
    q = 0.0
    basicfont = pygame.font.SysFont(None, 30)
    label = "Test"

    black = (0,0,0)
    # Main loop
    running = True
    while running:
        gd.draw_polygons()
        
        for event in pygame.event.get():
            # While in the gaming loop, if the mouse is clicked, get the position of the cursor and save them into variables mx and my, and print them out
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                message = "Not a Country"
                mx, my = pygame.mouse.get_pos()
                print(mx)
                print(', ')
                print(my)
                # A loop to go through the list of polygons, have their lat and long adjusted to a list of touples
                for poly in gd.polygons:
                    adjusted = []
                    a = 1
                    for p in poly:
                        if a == 1:
                            q = p
                        a = a + 1
                        x,y = p
                        adjusted.append(gd.convertGeoToPixel(x,y))
                    # Call point inside polygon to return true or false for each polygon in list of polygons
                    inside = point_inside_polygon(mx,my,adjusted)
                    if inside:
                        # If the point is inside the polygon continue forward by outlining the polygon
                        pygame.draw.polygon(gd.screen, black, adjusted, 5)
                        # Making and drawing bounding box
                        box = gd.make_box(adjusted)
                        gd.draw_boxes(box)
                        # Printing name to the screen
                        for c in df.wc.content['features']:
                            if q == c['geometry']['coordinates']:
                                message = c['properties']['name']
                            label = basicfont.render(message, True, (0,0,0), (255,255,0))
                            screen.blit(label, (100, 100))                           

                        
            pygame.display.flip()