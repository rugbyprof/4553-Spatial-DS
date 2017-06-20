from dbscan import *
import sys,os
import json
from nyc_file_helper import FileHelper

def calculate_mbrs(points, epsilon, min_pts,debug=False):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = {}
    clusters =  dbscan(points, epsilon, min_pts,debug=debug)
    extremes = {'max_x':sys.maxint * -1,'max_y':sys.maxint*-1,'min_x':sys.maxint,'min_y':sys.maxint}

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """

    for id,cpoints in clusters.items():
        print(id)
        xs = []
        ys = []
        for p in cpoints:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        if max_x > extremes['max_x']:
            extremes['max_x'] = max_x
        if max_y > extremes['max_y']:
            extremes['max_y'] = max_y
        if min_x < extremes['min_x']:
            extremes['min_x'] = min_x
        if min_y < extremes['min_y']:
            extremes['min_y'] = min_y

        mbrs[id]=[(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)]
    mbrs['extremes'] = extremes
    return mbrs

def adjust_location_coords(mbr_data,width,height):
    """
    Adjust your point data to fit in the screen. 
    Expects a dictionary formatted like `mbrs_manhatten_fraud.json` with extremes in it.
    """
    maxx = float(mbr_data['extremes']['max_x']) # The max coords from bounding rectangles
    minx = float(mbr_data['extremes']['min_x'])
    maxy = float(mbr_data['extremes']['max_y'])
    miny = float(mbr_data['extremes']['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = {}

    del mbr_data['extremes']

    for id,mbr in mbr_data.items():
        adjusted[id] = []
        for p in mbr:
            x,y = p
            x = float(x)
            y = float(y)
            xprime = (x - minx) / deltax         # val (0,1)
            yprime = 1.0 - ((y - miny) / deltay) # val (0,1)
            adjx = int(xprime*width)
            adjy = int(yprime*height)
            adjusted[id].append((adjx,adjy))
    return adjusted

def pull_points_from_nyc_data(data):
    """
    This method pulls NON adjusted points from the data file read in below.
    If you want them adjusted before clustering, do it yourself.
    Input:
       A list containing one row of a csv per entry with many fields.
    Returns:
       A list with points ONLY.
    """
    points = []
    for row in data:
        p = [int(row[19]),int(row[20])]
        if not p in points:
            points.append(p)
    
    return points

if __name__=='__main__':

    output_file = 'mbrs_manhatten_drugs.json'
    path_to_nyc = '/code/repos/4553-Spatial-DS/Resources/Data/NYPD_CrimeData/'

    # update this path to match your machine
    fh = FileHelper(path_to_nyc)
    data = fh.get_data(borough='manhattan',crime='drugs')

    """
    This is a helper method to grab only the points from the data that we just
    read in. 
    """
    points = pull_points_from_nyc_data(data)

    # Find the clusters from our NYC data file
    mbrs = calculate_mbrs(points,400,5,debug=True)

    # Remove the cluster that contains all the points NOT in a cluster
    del mbrs[-1]

    # Write the found clusters to an output file to be displayed later
    f = open(output_file,'w')
    f.write(json.dumps(mbrs, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()
