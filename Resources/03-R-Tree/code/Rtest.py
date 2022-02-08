from Rtree import *
from random import uniform
from time import time
import csv

root = Rtree(m=3, M=7)

stations = []

i = 0
with open("2013NRSC.csv", "rU") as csvfile:
    radioCsv = csv.reader(csvfile, delimiter=",", quotechar='"')
    for station in radioCsv:
        y = float(station[7])
        x = float(station[8])
        stations.append(
            node(
                MBR={
                    "xmin": x - 0.01,
                    "xmax": x + 0.01,
                    "ymin": y - 0.01,
                    "ymax": y + 0.01,
                },
                index=i,
            )
        )
        i = i + 1

for j in range(i):
    root = Insert(root, stations[j])
    print(type(root))
print(root.leaves)
