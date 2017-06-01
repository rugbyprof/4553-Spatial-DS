import nx_spatial as ns
import networkx as nx
from haversine import haversine
import sys


graph = ns.read_shp('./shape_files/tl_2013_48_prisecroads/tl_2013_48_prisecroads.shp')
edges = graph.edges()
nodes = graph.nodes()

d1 = sys.maxint
p1 = None
d2 = sys.maxint
p2 = None

for n in nodes:
    d =  haversine(n,(-101.897681,32.08691))
    if d < d1:
        d1 = d
        p1 = n
    d =  haversine(n,(-97.032193,32.759417))
    if d < d2:
        d2 = d
        p2 = n


def dist(a, b):
    return haversine(a,b)

print(nx.astar_path(graph,p1,p2,dist))
