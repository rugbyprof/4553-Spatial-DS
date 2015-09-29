from quadtree import QuadTree
from point import Point
from point import RandomPointGenerator
from rectangle import Rectangle
import random


##############################################################################


print 'Construct a quadtree (granularity 2) with 100 random points ...'
granularity = 2
area = Rectangle(Point(0, 0), Point(100, 100))
points = []
for i in range(100):
    points.append(Point(random.randint(0, 100),random.randint(0, 100)))
tree = QuadTree(points, granularity)

print 'report all points ...'
for point in tree:
    print point

print 'report all points in Rectangle(Point(0, 0), Point(25, 25))'
reported_points = []
for point in tree.report_points_in_rectangle(Rectangle(Point(0, 0), Point(5, 5))):
    reported_points.append(point)
    print point
for point in points:
    if point not in reported_points:
        assert(point not in Rectangle(Point(0, 0), Point(5, 5)))


################################################################################
