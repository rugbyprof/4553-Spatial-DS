import geo2d.geometry as g

p1 = g.Point((0, 1))
p2 = g.Point((4.2, 5))
print(p1.distance_to(p2))
l = g.Segment(p1, p2)

p1 = g.Point((-107.9145813, 37.2281415))
p2 = g.Point((-84.4477844, 36.9476968))
print(p1.distance_to(p2))
l = g.Segment(p1, p2)
