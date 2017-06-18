import sys,os
import pprint as pp
import math

DIRPATH = os.path.dirname(os.path.realpath(__file__))

class crime_data(object):
    def __init__(self,file_name):
        self.file_name = file_name
        self.keys = []
        self.data = []
        self.loc_data = {'points':[],'extremes':[]}
        self.xvals = []
        self.yvals = []
        self.latvals = []
        self.lonvals = []
        self.key_words = {}

        self._process_data_file()
        self._calulate_extremes()
        self._adjust_location_coords()


    def _adjust_location_coords(self):
        # xy = self.loc_data['extremes']['xy']
        # deltax = float(xy['maxx']) - float(xy['minx'])
        # deltay = float(xy['maxy']) - float(xy['miny'])
        # maxx = float(xy['maxx'])
        # maxy = float(xy['maxy'])
        # minx = float(xy['minx'])
        # miny = float(xy['miny'])
        maxx = float(1067226)
        maxy = float(271820)
        minx = float(913357)
        miny = float(121250)
        deltax = float(maxx) - float(minx)
        deltay = float(maxy) - float(miny)

        for p in self.loc_data['points']:
            x,y = p['xy']
            x = float(x)
            y = float(y)
            xprime = (x - minx) / deltax
            yprime = 1.0 - ((y - miny) / deltay)
            p['adjusted'] = (xprime,yprime)

    def _process_data_file(self):
        got_keys = False
        with open(self.file_name) as f:
            for line in f:
                # fix line by replacing commas in between double quotes with colons
                line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
                # turn line into a list
                line = line.strip().split(',')
                if not got_keys:
                    self.keys = line
                    got_keys = True
                    continue
                self.data.append(line)
                self._process_location_coords(line)

    def _process_location_coords(self,row):

        x = row[19]                 # get x val from list
        y = row[20]                 # get y val from list
        lat = row[21]               # get lat / lon from list
        lon = row[22]

        if x and y:
            x = int(x)
            y = int(y)
            self.xvals.append(x)
            self.yvals.append(y)

        if lat and lon:
            lat = float(lat)
            lon = float(lon)
            self.latvals.append(lat)
            self.lonvals.append(lon)    

        if lat and lon and x and y:
            self.loc_data['points'].append({'xy':(x,y),'latlon':(lat,lon)})

    def _calulate_extremes(self):
        self.loc_data['extremes'] = {'xy':{'maxx':max(self.xvals),'maxy':max(self.yvals),'minx':min(self.xvals),'miny':min(self.yvals)},
                        'latlon':{'maxlon':max(self.lonvals),'maxlat':max(self.latvals),'minlon':min(self.lonvals),'minlat':min(self.latvals)}}
    

    def get_location_coords(self):
        return self.loc_data

    def get_adjusted_coords(self,width,height):
        adj = []
        i = 0
        for p in self.loc_data['points']:
            x,y = p['adjusted']
            adj.append((int(x*width),int(y*height)))
            i += 1
        return adj

class DBscan(object):
    def __init__(self,points,eps=5,min=5):
        self.points = points    # list of tuples or lists e.g. (x,y) or [x,y]
        self.min = min
        self.eps = eps
        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0],self.points[i][1],False,None)
        self.doScan()

    def doScan(self):
        for i in range(len(self.points)):
            nbs = self.immediate_neighbours(self.points[i])
            print(len(nbs))
            if i > 100:
                break

    def euclidean(self,x,y):
        ''' calculate the euclidean distance between x and y.'''
        # sqrt((x0-y0)^2 + ... (xN-yN)^2)
        assert len(x) == len(y)
        sum = 0.0
        for i in range(len(x)):
            sum += pow(x[i] - y[i],2)
        return sqrt(sum)

    def distance(self,p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    def immediate_neighbours(self,point):
        ''' find the immediate neighbours of point.'''
        # XXX TODO: this is probably a stupid way to do it; if we could
        # use a grid approach it should make this much faster.
        neighbours = []
        for i in range(len(self.points)):
            if self.points[i] == point:
                # you cant be your own neighbour...!
                continue
            d = self.distance(self.points[i],point)
            if d < self.eps:
                neighbours.append(i)
        return neighbours

def main():
    Assault_Bronx = '/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/data_by_crime/Assault_Bronx.csv'
    cd1 = crime_data(Assault_Bronx)
    points = cd1.get_adjusted_coords(1000,1000)
    db = DBscan(points,3,5)

#cd = crime_data(DIRPATH+'/'+'Nypd_Crime_01')


if __name__=='__main__':
    main()