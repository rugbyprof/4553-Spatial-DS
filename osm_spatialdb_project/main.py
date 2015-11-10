import networkx as nx
import nx_spatial as ns
import pantograph
import sys
import math


class driver(pantograph.PantographHandler):

    def setup(self):
        self.map_init(-96.50,32,4)
        self.draw_line(0, 0, self.width, self.height,"#F00")
        self.net = ns.read_shp('./shape_files/tl_2013_48_prisecroads/tl_2013_48_prisecroads.shp')
        self.edges = self.net.edges()
        self.nodes = self.net.nodes()
        self.map_done_loading()
        self.fit_bounds()

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        self.draw_line(0, 0, self.width, self.height,"#F00")
        #print len(self.edges)
        #print len(self.nodes)

    def fit_bounds(self):
        self.minLon = sys.maxint
        self.minLat = sys.maxint
        self.maxLon = 0
        self.maxLat = 0

        for n in self.nodes:
            if math.fabs(n[0]) < math.fabs(self.minLon):
                self.minLon = n[0]
            if math.fabs(n[1]) < math.fabs(self.minLat):
                self.minLat = n[1]
            if math.fabs(n[0]) > math.fabs(self.maxLon):
                self.maxLon = n[0]
            if math.fabs(n[1]) > math.fabs(self.maxLat):
                self.maxLat = n[1]
        self.map_fitBounds(self.minLon,self.minLat,self.maxLon,self.maxLat)

    def on_click(self,event):
        self.do_operation("clickMap")


if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(driver)
    app.run()
