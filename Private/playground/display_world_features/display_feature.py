import os,sys
import math
import pygame
from pygame.locals import *
import json
from pymongo import MongoClient

#http://cs.mwsu.edu/~griffin/geospatial/

class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

    def get_features_near_me(self,collection,point,radius,earth_radius=3963.2): #km = 6371
        """
        Finds "features" within some radius of a given point.
        Params:
            collection_name: e.g airports or meteors etc.
            point: e.g (-98.5034180, 33.9382331)
            radius: The radius in miles from the center of a sphere (defined by the point passed in)
        """
        x,y = point


        res = self.client['world_data'][collection].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , radius/earth_radius ] } }} )
        
        return self._make_result_list(res)

    def get_doc_by_keyword(self,collection,field_name,search_key,like=True):
        """
        Finds "docs" with some keyword in some field.
        Params:
            collection_name: e.g airports or meteors etc.
            field_name: key name of the field to search. e.g. 'place_id' or 'magnitude' 
            search_key: The radius in miles from the center of a sphere (defined by the point passed in)
        """
        if like:
            # This finds the records in which the field just "contains" the search_key
            res = self.client['world_data'][collection].find(({field_name : {'$regex' : ".*"+search_key+".*"}}))
        else:
            # This finds the records in which the field is equal to the search_key
            res = self.client['world_data'][collection].find({field_name : search_key})

        return self._make_result_list(res)


    def get_feature_in_poly(self,collection,poly):
        """
        Get features 
        Params:
            poly (object): geojson poly
            co = db.states.findOne({"code":"co"})
            db.airports.find( { geometry : { $geoWithin : { $geometry : {type: "Polygon", coordinates: co.borders }} } })
        """
        res = self.client['world_data'][collection].find( { 'geometry' : { '$geoWithin' : { '$geometry' : {'type': "Polygon", 'coordinates': poly }} } })


        return self._make_result_list(res)

    def get_poly_by_point(self,collection,point):
        return self.client['world_data'][collection].find_one({'geometry':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def _make_result_list(self,res):
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_state_poly(self,state):
        state_poly = self.client['world_data']['states'].find_one({'code' : state})
        return state_poly['borders']

    def get_country_poly(self,id):
        country_poly = self.client['world_data']['countries'].find_one({'id' : id})
        return country_poly['geometry']

    # def get_afb_airports(self):

        
    #     res = self.db_airports.find({"type" : "Military"})

    #     res_list = []
    #     for r in res:
    #         res_list.append(r)

    #     return res_list

    # def get_doc_by_keyword(self,db_name,field,key):
    #     if db_name == 'airports':
    #         res = self.db_airports.find({field : {'$regex' : ".*"+key+".*"}})
    #     else:
    #         res = self.states.find({field : {'$regex' : ".*"+key+".*"}})
        
    #     res_list = []
    #     for r in res:
    #         res_list.append(r)

    #     return res_list

    # def get_nearest_neighbor(self,lon,lat,r):
    #    # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
    #     air_res = self.db_ap.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

    #     min = 999999
        
    #     for ap in air_res:
    #         lon2 = ap['geometry']['coordinates'][0]
    #         lat2 = ap['geometry']['coordinates'][1]
    #         d = self._haversine(lon,lat,lon2,lat2)
    #         if d < min:
    #             min = d
    #             print(d)
    #             print(ap['properties']['ap_name'])
    #             closest_ap = ap

    #     return closest_ap

    # def get_state_by_point(self,point):
    #     return self.db_states.find_one({'loc':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    # def get_state_by_name(self,name):
    #     pass

    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r


def get_extremes(points):
    maxX = -999
    minX = 999
    maxY = -999
    minY = 999

def mercX(lon,zoom = 1):
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return a * b

def mercY(lat,zoom = 1):
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return (a * c) - 256 

def adjust_location_coords(extremes,points,width,height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    maxX = float(extremes['maxX']) # The max coords from bounding rectangles
    minX = float(extremes['minX'])
    maxY = float(extremes['maxY'])
    minY = float(extremes['minY'])
    deltax = float(maxX) - float(minX)
    deltay = float(maxY) - float(minY)

    adjusted = []

    for p in points:
        x,y = p
        x = float(x)
        y = float(y)
        xprime = (x - minx) / deltax    # val (0,1)
        yprime = ((y - miny) / deltay)  # val (0,1)
        adjx = int(xprime*width)
        adjy = int(yprime*height)
        adjusted.append((adjx,adjy))
    return adjusted

def get_country_poly(id,countries):
    pointlist = []

    for country in countries:
        if country['properties']['ISO_A3'] == id:
            return country['geometry']


def flatten_country_polygons(geometry):
    adjusted_polys = []
    if geometry['type'] == 'Polygon':
        pass
    else:
        for polygons in geometry['coordinates']:
            for polygon in polygons:
                newp = []
                for p in polygon:
                    newp.append([mercX(p[0]),mercY(p[1])])
                    print(p[0],p[1])
                adjusted_polys.append(newp)
        return adjusted_polys

    # for c in coords:
    #     pointlist.extend(c)

    # for i in range(len(pointlist)):
    #     x,y = pointlist[i]
    #     pointlist[i] = (mercX(x),mercY(y))
    # return pointlist


# poly = list(reversed([[-108.7207031,40.8491380],[-102.3925781,40.9155881],[-102.2167969,37.1625054],[-109.2480469,37.0924307],[-108.7207031,40.8491380]]))
# print(poly)

# mh = mongoHelper()

# res = mh.get_features_near_me('airports',(-98.5034180, 33.9382331),200)
# print(res)

# res = mh.get_doc_by_keyword('airports','properties.tz','Europe')
# print(len(res))

# res = mh.get_doc_by_keyword('airports','properties.continent','Europe',False)
# print(len(res))

# state = mh.get_state_poly('co')
# print(state)

# res = mh.get_feature_in_poly('airports',state)
# print(res)

# country = mh.get_country_poly('DEU')

# res = mh.get_feature_in_poly('airports',country['coordinates'])
# print(len(res))

# res = mh.get_poly_by_point('countries',[44.2968750,24.6669864])
# print(res)



f = open("/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Private/playground/display_world_features/geojson/countries.geojson","r")

countries = json.loads(f.read())

country = get_country_poly("USA",countries)

poly = flatten_country_polygons(country)



screen_width = 1024
screen_height = 512

#print(mercX(-98.5034180),mercY(33.9382331))

cx = mercX(0)
cy = mercY(0)

dir_path = os.path.dirname(os.path.realpath(__file__))
#bg_image = os.path.join(dir_path,"images/4167-2083.png")
bg_image = os.path.join(dir_path,"images/1024x512.png")
pin_image = os.path.join(dir_path,"images/pin-6.png")

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
bg = pygame.image.load(bg_image)
pin = pygame.image.load(pin_image)
screen.blit(pygame.transform.scale(bg, (screen_width,screen_height)), (0, 0))
screen.blit(pin,(mercX(-98.5034180)-16,mercY(33.9382331)-32))
for p in poly:
    pygame.draw.polygon(screen, (255,164,0), p,1)
pygame.display.flip()
while True:
    pygame.event.pump()
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.display.quit()
    elif event.type == VIDEORESIZE:
        screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
        #print(event.dict['size'])
        screen.blit(pygame.transform.scale(bg, event.dict['size']), (0, 0))

        screen.blit(pin,(mercX(-98.5034180)-16,mercY(33.9382331)-32))
        for p in poly:
            pygame.draw.polygon(screen, (255,164,0), p,1)
        pygame.display.flip()
