#!/usr/bin/python
# -*- coding: utf-8 -*-
from Rtree import *
from random import uniform
from time import time

numRuns = 1000

data = {}
# Initialize 10000 coordinates (-1000, 1000), an area of ​​a rectangle 0.01.
for i in range(numRuns):
    x = uniform(-1000, 1000)
    y = uniform (-1000, 1000)
    data [i] = {'xmin': x, 'xmax': x + 0.01, 'ymin': y, 'ymax': y + 0.01}
# Set a root node, m = 3, M = 7
root = Rtree(m = 3, M = 7)
n = []

for i in range(numRuns):
    n.append(node(MBR = data[i], index = i))
t0 = time()
# Insert
for i in range(numRuns):
    root = Insert(root, n[i])
    print root
t1 = time()
print 'Inserting ...'
print t1 - t0
#search for
x = root.Search(merge(n[0].MBR, n[1].MBR))
print x
t2 = time()
print 'Searching ...'
print t2 - t1
# Delete
for i in range(numRuns):
    root = Delete(root, n[i])
t3 = time()
print 'Deleting ...'
print t3 - t2
