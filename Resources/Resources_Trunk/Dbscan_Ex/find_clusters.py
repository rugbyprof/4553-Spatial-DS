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
    clusters =  dbscan(points, epsilon, min_pts,distance=euclidean,debug=debug)
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

def pull_points_from_nyc_data(data):
    """
    This method pulls NON adjusted points from the data file read in below.
    If you want them adjusted before clustering, do it yourself.
    """
    points = []
    for row in data:
        points.append([int(row[19]),int(row[20])])
    
    return points

if __name__=='__main__':

    output_file = 'mbrs_manhatten_fraud.json'
    path_to_nyc = '/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/'


    # update this path to match your machine
    fh = FileHelper(path_to_nyc)
    data = fh.get_data(borough='manhattan',crime='fraud')

    """
    This is a helper method to grab only the points from the data that we just
    read in.
    """
    points = pull_points_from_nyc_data(data)

    mbrs = calculate_mbrs(points,5,5,debug=True)

    f = open(output_file,'w')
    f.write(json.dumps(mbrs, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()
