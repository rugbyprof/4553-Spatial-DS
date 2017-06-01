import sys
import math
import csv
import numpy as np


"""
@class node - simple kdtree node
@method - __init__: Sets value,children,discriminator
@method - getVals: Return list of items in the node
@method - printNode: Prints items in node for debugging purposes
"""
class node:
    def __init__(self,dim_items=None,disc=None):

        if not dim_items:
            self.dim = 0
            self.dimList = []
        else:
            self.dimList = dim_items
            self.dim = len(self.dimList)

        self.leftChild = None
        self.rightChild = None
        self.disc = disc

    """
    @public
    @method - getVals: Return list of items in the node
    @param void
    @returns list[]: list of items in node
    """
    def getVals(self):
        return self.dimList

    """
    @public
    @method - getDiscValue: Return value based on discriminator
    @param void
    @returns mixed: Item in list
    """
    def getDiscValue(self):
        return self.dimList[self.disc]

    """
    @public
    @method - setVals: Set values held in node
    @param vals[]: List of items
    @returns bool: True if successful
    """
    def setVals(self,vals):
        if not len(vals) == self.dim:
            return False
        for i in range(len(vals)):
            self.dimList[i] = vals[i]

        return True


    """
    @public
    @method - printNode: Prints items in node for debugging purposes
    @param {bool} retConent: Return instead of print
    @returns {string} : maybe
    """
    def printNode(self,retContent=None):
        pString = ', '.join(map(str, self.dimList))
        pString += "\n"
        pString += "leftChild: " + str(self.leftChild) + "\n"
        pString += "rightChild: "  + str(self.rightChild) + "\n"
        pString += "disc: "  + str(self.disc)
        if not retContent:
            print(pString)
        else:
            return pString



class kdtree:
    def __init__(self,dim):

        self.root = None
        self.dim = dim

    """
    @public
    @method - insert: Insert value into kdtree
    @param val: item of length dim (where dim = dimension) to place into a node
    @returns bool: true if successful
    """
    def insert(self,val):
        if self._is_iterable(val):
            if self.root == None:
                self.root = node(val,0)
                return True
            else:
                newNode = node(val,0)
                currRoot = self.root

                self._recInsert(currRoot,newNode)

        else:
            print(val)
            print("Whoops: Item must be iterable.")
            return False

    """
    @private
    @method - _recInsert: Insert value into kdtree
    @param root: a copy of the root of the tree
    @param node: the new node to be inserted
    @returns bool: true if successful
    """
    def _recInsert(self,root,newNode):
        if newNode.getDiscValue() > root.getDiscValue():
            if root.rightChild == None:
                root.rightChild = newNode
                newNode.disc = (root.disc + 1) % self.dim
            else:
                self._recInsert(root.rightChild,newNode)
        else:
            if root.leftChild == None:
                root.leftChild = newNode
                newNode.disc = (root.disc + 1) % self.dim
            else:
                self._recInsert(root.leftChild,newNode)

    """
    @public
    @method - Traverse: Traverse the kdtree by whichever specified means
    @param traversal_type: pre=preorder,in=inorder,post=postorder
    @returns None
    """
    def Traverse(self,traversal_type="in",fileName=None):

        if not fileName == None:
            f = open(fileName,'w')
            self._Traverse2(self.root,traversal_type,f)
        else:
            self._Traverse(self.root,traversal_type)

    def _Traverse(self,root,traversal_type):
        if root == None:
            return
        else:
            if traversal_type == "pre":
                root.printNode()
                print("=========")
            self._Traverse(root.leftChild,traversal_type)
            if traversal_type == "in":
                root.printNode()
                print("=========")
            self._Traverse(root.rightChild,traversal_type)
            if traversal_type == "post":
                root.printNode()
                print("=========")

    def _Traverse2(self,root,traversal_type,f):
        if root == None:
            return
        else:
            if traversal_type == "pre":
                f.write(root.printNode(True))
                f.write("=========")
            self._Traverse2(root.leftChild,traversal_type,f)
            if traversal_type == "in":
                f.write(root.printNode(True))
                f.write("=========")
            self._Traverse2(root.rightChild,traversal_type,f)
            if traversal_type == "post":
                f.write(root.printNode(True))
                f.write("=========")


    """
    @private
    @method - is_iterable: determines whether the var is iterable (list,etc)
    @param var: variable to be tested
    @returns bool: true if iterable
    """
    def _is_iterable(self,var):

        return isinstance(var, (list, tuple))

class MapHelper:
    def __init__(self):
        pass

    def displace(self,lat,lng,theta, distance,unit="miles"):
        """
        Displace a LatLng theta degrees clockwise and some feet in that direction.
        Notes:
            http://www.movable-type.co.uk/scripts/latlong.html
            0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
        Args:
            theta:    A number in degrees where:
                      0   = North
                      90  = East
                      180 = South
                      270 = West
            distance: A number in specified unit.
            unit:     enum("miles","kilometers")
        Returns:
            A new LatLng.
        """
        theta = np.float32(theta)
        radiusInMiles = 3959
        radiusInKilometers = 6371

        if unit == "miles":
            radius = radiusInMiles
        else:
            radius = radiusInKilometers

        delta = np.divide(np.float32(distance), np.float32(radius))

        theta = deg2rad(theta)
        lat1 = deg2rad(lat)
        lng1 = deg2rad(lng)

        lat2 = np.arcsin( np.sin(lat1) * np.cos(delta) +
                          np.cos(lat1) * np.sin(delta) * np.cos(theta) )

        lng2 = lng1 + np.arctan2( np.sin(theta) * np.sin(delta) * np.cos(lat1),
                                  np.cos(delta) - np.sin(lat1) * np.sin(lat2))

        lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

        return [self.rad2deg(lat2), self.rad2deg(lng2)]

    def deg2rad(self,theta):
            return np.divide(np.dot(theta, np.pi), np.float32(180.0))

    def rad2deg(self,theta):
            return np.divide(np.dot(theta, np.float32(180.0)), np.pi)

    def lat2canvas(self,lat):
        """
        Turn a latitude in the form [-90 , 90] to the form [0 , 180]
        """
        return float(lat) % 180

    def lon2canvas(self,lon):
        """
        Turn a longitude in the form [-180 , 180] to the form [0 , 360]
        """
        return float(lon) % 360

    def canvas2lat(self,lat):
        """
        Turn a latitutude in the form [0 , 180] to the form [-90 , 90]
        """
        return ((float(lat)+90) % 180) - 90

    def canvas2lon(self,lon):
        """
        Turn a longitude in the form [0 , 360] to the form [-180 , 180]
        """
        return ((float(lon)+180) % 360) - 180

    def poly2canvas(self,poly):
        newPoly = []
        for p in poly:
            y,x = p
            y = self.lon2canvas(y)
            x = self.lat2canvas(x)
            newPoly.append((x,y))
        return newPoly

    # Determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs. This function
    # returns True or False.  The algorithm is called
    # the "Ray Casting Method".
    def point_in_poly(self,x,y,poly):

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

class BoundingBox(object):
    def __init__(self, *args, **kwargs):
        self.lat_min = None
        self.lon_min = None
        self.lat_max = None
        self.lon_max = None

"""
@public
@method get_bounding_box: Creates a bounding box around a single point that is "half_side_in_miles"
                          away in every cardinal direction.
@param {float}-lat      : latitude
@param {float}-lon      : longitude
@param distance         : distance in miles
@returns {object}       : bounding box
"""
def get_bounding_box(lat, lon, distance):
    assert distance > 0
    assert lat >= -180.0 and lat  <= 180.0
    assert lon >= -180.0 and lon <= 180.0

    lat = math.radians(lat)
    lon = math.radians(lon)

    radius  = 3959
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - distance/radius
    lat_max = lat + distance/radius
    lon_min = lon - distance/parallel_radius
    lon_max = lon + distance/parallel_radius
    rad2deg = math.degrees

    box = BoundingBox()
    box.lat_min = rad2deg(lat_min)
    box.lon_min = rad2deg(lon_min)
    box.lat_max = rad2deg(lat_max)
    box.lon_max = rad2deg(lon_max)

    return (box)

def loadCities():
    citys = []
    with open('./citylist.csv', 'rb') as csvfile:
        citysCsv = csv.reader(csvfile, delimiter=',', quotechar='"')
        for city in citysCsv:
            citys.append({"Name":city[0],"Country":city[1],"lat":city[2],"lon":city[3]})
    return citys

if __name__ == '__main__':

    cities = loadCities()
    myMap = MapHelper()

    tree = kdtree(2)

    for c in cities:
        latlon = [myMap.lat2canvas(c['lat']),myMap.lon2canvas(c['lon'])]
        tree.insert(latlon)
    tree.Traverse("in","output.txt")
    #30.26715,-97.74306
    print(myMap.lat2canvas(30.26715),myMap.lon2canvas(-97.74306))
    box = get_bounding_box(32.0965363,-98.6352539,100)
    print(box.lat_min,box.lon_min,box.lat_max,box.lon_max)

    ## Test

    polygon = [(34.303197,-102.26727),(34.303197,-95.486634),(28.514283,-102.26727),(28.514283,-95.486634),(34.303197,-102.26727)]

    point_x = -101.337891
    point_y = 29.5913712

    ## Call the function with the points and the polygon
    print myMap.point_in_poly(point_x,point_y,polygon)
