import pyqtree
import csv
from math import *
import numpy as np

def loadCities():
    citys = []
    with open('citylist.csv', 'rb') as csvfile:
        citysCsv = csv.reader(csvfile, delimiter=',', quotechar='"')
        for city in citysCsv:
            citys.append({"Name":city[0],"Country":city[1],"lat":city[2],"lon":city[3]})
    return citys


def displace(lat,lng,theta, distance,unit="miles"):
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

    return [rad2deg(lat2), rad2deg(lng2)]

def deg2rad(theta):
        return np.divide(np.dot(theta, np.pi), np.float32(180.0))

def rad2deg(theta):
        return np.divide(np.dot(theta, np.float32(180.0)), np.pi)

def lat2canvas(lat):
    """
    Turn a latitude in the form [-90 , 90] to the form [0 , 180]
    """
    return float(lat) % 180

def lon2canvas(lon):
    """
    Turn a longitude in the form [-180 , 180] to the form [0 , 360]
    """
    return float(lon) % 360

def canvas2lat(lat):
    """
    Turn a latitutude in the form [0 , 180] to the form [-90 , 90]
    """
    return ((float(lat)+90) % 180) - 90

def canvas2lon(lon):
    """
    Turn a longitude in the form [0 , 360] to the form [-180 , 180]
    """
    return ((float(lon)+180) % 360) - 180

def main():
    spindex = pyqtree.Index(bbox=[0,0,100,100])
    points = [(39, 21), (86, 19), (65, 5), (76, 28), (3, 9), (31, 59), (43, 99), (60, 50), (42, 48), (15, 73), (67, 98), (16, 34), (27, 80), (51, 77), (30, 67), (82, 68), (85, 46), (89, 44), (21, 30), (5, 66), (75, 29), (17, 14), (40, 90), (18, 33), (52, 64), (1, 71), (88, 10), (64, 26), (96, 2), (25, 40)]

    n = 0
    for p in points:


        minx = p[0]-1
        miny = p[1]-1
        maxx = p[0]+1
        maxy = p[1]+1

        it = str(p[0])+","+str(p[1])

        bbox =[minx,miny,maxx,maxy]
        spindex.insert(item=it, bbox=bbox)
        n += 1


    printNodes(spindex)

def printNodes(root):
    if isinstance(root, pyqtree._QuadTree):
        for node in root.nodes:
            print node
            printNodes(node)
    else:
        print root

if __name__ == '__main__':
    main()
