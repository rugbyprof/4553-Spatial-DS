# from json import load, JSONEncoder
import json
from argparse import ArgumentParser, FileType
from re import compile
import sys
from rich import print
import geopandas
import glob

from shapely.geometry import Polygon, mapping
from shapely.ops import unary_union


def within(parent, child):
    ''' Checks to see if child is totally within parent
    '''
    return (float(child[0]) >= float(parent[0])
            and float(child[1]) >= float(parent[1])
            and float(child[2]) <= float(parent[2])
            and float(child[3]) <= float(parent[3]))


def Bbox(poly):
    ''' Returns a bounding box, given a polygon (list of points)
    '''
    minx = miny = 99999
    maxx = maxy = -99999
    for point in poly:
        if float(point[0]) < minx:
            minx = float(point[0])
        if float(point[1]) < miny:
            miny = float(point[1])
        if float(point[0]) > maxx:
            maxx = float(point[0])
        if float(point[1]) > maxy:
            maxy = float(point[1])
    return (minx, miny, maxx, maxy)


def mykwargs(argv):
    '''
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}
        
        Params with dashes (flags) can now be processed seperately
    Shortfalls: 
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    '''
    args = []
    kargs = {}

    for arg in argv:
        if '=' in arg:
            key, val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs


class PolyMerger(object):
    """ Merge a multipolygon (or many multipolygons) into a single polygon

    Args:
        kwargs (dict): keyword arguments
            - infile    : input file name
            - outfile   : output file name
            - filterKey : a key name to test so features can be filtered
            - filterVal : the value the key will be compared against to check for a match
    """

    def __init__(self, **kwargs):
        self.inFile = kwargs.get('in', '*.geojson')
        self.outFile = kwargs.get('out', 'merged.geojson')
        self.filterKey = kwargs.get('filterKey', None)
        self.filterVal = kwargs.get('filterVal', None)
        self.bbox = kwargs.get('bbox', (-180, -89, 180, 89))

        # newBox = []
        # for val in json.loads(self.bbox):
        #     newBox.append(float(val))

        # self.bbox = tuple(newBox)

        if self.filterKey and self.filterVal:
            print(f"{self.filterKey} = {self.filterVal}")

        print(self.bbox)

        self.loadData()
        self.gatherPolygons()
        self.mergePolygons()

    def loadData(self, infile=None):
        '''
        Description:
            Loads data from the input file(s) into our class instance.
        Params:
            infile (string) : filename will replace self.inFile
        Returns: 
            None
        '''
        if infile:
            self.inFile = infile

        if '*' in self.inFile:
            # load all the geojsons!
            self.loadGeoJsonFiles()
        else:
            # # open traditional json file
            # with open(self.inFile) as f:
            #     self.geoData = json.load(f)
            # self.features = self.geoData['features']

            # open geopandas dataframe commy data structure
            self.geoPandaData = []
            self.geoPandaData.append(geopandas.read_file(self.inFile))

    def loadGeoJsonFiles(self):
        '''
        Description:
            Loads data from the input file(s) into our class instance.
        Params:
            infile (string) : filename or None
        Returns: 
            None
        '''
        self.geoJsonFiles = glob.glob("./*.geojson")
        self.features = []
        self.geoPandaData = []

        for file in self.geoJsonFiles:
            # open local geojson file
            # with open(file) as f:
            #     temp = json.load(f)
            #     self.features.extend(temp['features'])
            print(f"processing: {file}")
            self.geoPandaData.append(geopandas.read_file(file))

    def gatherPolygons(self):
        '''
        Description:
            Iterates over dataframe and pulls out multipolygons to turn into polygons
        Params:
            None
        Returns: 
            None
        '''
        self.polygons = []
        filterVals = []
        print(self.geoPandaData)
        print(len(self.geoPandaData))

        multiPolygons = None
        # if len(self.geoPandaData) == 1:
        #     self.geoPandaData = [self.geoPandaData]

        for chunk in self.geoPandaData:
            print(len(chunk))
            for key, val in chunk.items():
                if key == 'geometry':
                    multiPolygons = list(val)
                if key == 'bbox_poly':
                    bbox_polys = list(val)
                if key == self.filterKey:
                    filterVals = list(val)

            for i in range(len(multiPolygons)):
                print(f"{filterVals[i]} == {self.filterKey}")
                if (self.filterKey and self.filterVal) and (filterVals[i]
                                                            == self.filterVal):

                    print(f"Adding: {filterVals[i]}")
                    bbox = Bbox(json.loads(bbox_polys[i]))
                    if within(self.bbox, bbox):
                        for polygon in multiPolygons[i]:
                            self.polygons.append(polygon)

    def mergePolygons(self):
        '''
        Description:
            Turns 2 or more polygons into a single polygon (hopefully)
        Params:
            None
        Returns: 
            None
        '''
        new_geometry = mapping(unary_union(
            self.polygons))  # This line merges the polygones

        self.newFeatures = dict(type='Feature',
                                id="",
                                properties=dict(Name=""),
                                geometry=dict(
                                    type=new_geometry['type'],
                                    coordinates=new_geometry['coordinates']))
        if self.filterKey and self.filterVal:
            self.newFeatures['properties'][self.filterKey] = self.filterVal
        # print(self.newFeatures)

    def writeGeoJson(self, outPath=None):
        ''' Write a geojson file based on the new "merged" features created within the class. 
        '''
        outJson = dict(type='FeatureCollection', features=[self.newFeatures])

        if outPath:
            self.outFile = outPath

        with open(self.outFile, "w") as f:
            json.dump(outJson, f, indent=4)


def usage():
    print('''
        python merger.py (optional) in=path 
                         (optional) out=name 
                         (optional) filterKey=someKey 
                         (optional) filterVal=someValue
                         (optional) bbox=(minx,miny,maxx,maxy)
        
        `in` = input location (file or directory)
        `path` = name of input file or directory to read. If empty all geojson files in local dir will be read.
        `filterKey` = key in properties to test against
        `filterVal` = value pointed to by `filterKey`
        `bbox` = bounding box to test polygons against as a filter
        ''')
    print('''
        python merger.py in=South_America.geojson
                         out=Brazil.geojson 
                         filterKey='name' 
                         filterVal='Brazil'
        ''')
    sys.exit()


# def testFunction(**kwargs):
#     print(kwargs)
#     fname = kwargs.get('fname', None)
#     lname = kwargs.get('lname', None)
#     ssn = kwargs.get('ssn', None)
#     weight = kwargs.get('weight', 0)
#     visa = kwargs.get('visa', None)

#     if not ssn:
#         print("Error: no social!!")
#         sys.exit()

#     print(fname.title())
#     print(lname.title())

if __name__ == '__main__':
    argv = sys.argv[1:]

    if 'help' in argv:
        # if params are required ...
        usage()

    args, kargs = mykwargs(argv)

    pm = PolyMerger(**kargs)
    pm.writeGeoJson()

    # testFunction(visa=83838383838383,
    #              weight=132,
    #              fname='terry',
    #              ssn=555555555,
    #              lname='griffin')

# "bbox": [-180,41.19268056,180,81.85871003]