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


def displace(lat,lng,theta, distance):
    """
    Displace a LatLng theta degrees clockwise and some
    meters in that direction.
    Notes:
        http://www.movable-type.co.uk/scripts/latlong.html
        0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
    Args:
        theta:    A number in degrees.
        distance: A number in meters.
    Returns:
        A new LatLng.
    """
    theta = np.float32(theta)

    delta = np.divide(np.float32(distance), np.float32(3959))

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


def main():
    spindex = pyqtree.Index(bbox=[0,0,360,180])
    cities = loadCities()

    for c in cities:
        #{'lat': '-18.01274', 'Country': 'Zimbabwe', 'lon': '31.07555', 'Name': 'Chitungwiza'}
        item = c['Name']
        bbox =[float(c['lat']),float(c['lon']),float(c['lat']),float(c['lon'])]
        spindex.insert(item=item, bbox=bbox)

    overlapbbox = (51,51,86,86)
    matches = spindex.intersect(overlapbbox)
    print(matches)

    lat1 = 33.912523
    lon1 = -98.497925

    print(displace(lat1,lon1,270,300))



if __name__ == '__main__':
    main()
