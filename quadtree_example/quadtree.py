###############################################################################


from point import Point
from rectangle import Rectangle


################################################################################


class QuadTreeException(Exception):
    pass


################################################################################


class QuadTree(object):

    class _QuadTreeNode(object):
        '''
        Astract base class for quastree nodes
        '''

        def __init__(self, square):
            '''
            any quadtree node must store a square
            '''
            if self.__class__ is QuadTree._QuadTreeNode:
                raise QuadTreeException('QuadTree._QuadtreeNode is an abstract class')
            self._square = square

        def __iter__(self):
            '''
            Return an iterator over all points stored in the subtree rooted at this node.
            '''
            return iter(self._report_all_points())

        def size(self):
            '''
            To be implemented in derived class
            '''
            raise NotImplementedException('not implemented')

        def _report_all_points(self):
            '''
            To be implemented in derived class
            '''
            raise NotImplementedException('not implemented')

        def _report_points_in_rectangle(self):
            '''
            To be implemented in derived
            '''
            raise NotImplementedException('not implemented')

        def get_square(self):
            '''
            Return the square associated to the subtree rooted at this node
            '''
            return self._square

        square = property(get_square, None, None, 'square read only property')

    class _QuadTreeInternalNode(_QuadTreeNode):
        '''
        A quadtree internal node, i.e., a quadtree node with 4 children
        '''

        def __init__(self, square, upper_right, upper_left, lower_left, lower_right):
            '''
            Initalize this internal quadtree nodes
            '''
            super(QuadTree._QuadTreeInternalNode, self).__init__(square)
            self._upper_right = upper_right
            self._upper_left  = upper_left
            self._lower_left  = lower_left
            self._lower_right = lower_right

        def __str__(self):
            '''
            Stringify this quadtree internal node
            '''
            return 'QuadTreeInternalNode(%s,%s,%s,%s)' % \
             (str(self._upper_right), str(self._upper_left), str(self._lower_left), str(self._lower_right))

        def size(self):
            '''
            Return the number of points stored in the subtree rooted at this node
            '''
            return  self._upper_right.size() + \
                self._upper_left.size()      + \
                self._lower_left.size()      + \
                self._lower_right.size()

        def _report_all_points(self):
            '''
            Report all points stored in the subtree rooted at this node
            '''
            pass # COMPLETER

        def _report_points_in_rectangle(self, rectangle):
            '''
            Report all points stored in the subtree rooted at this node that are
            in a query rectangle
            '''
            pass # A COMPLETER

    class _QuadTreeLeaf(_QuadTreeNode):
        '''
        A quadtree leaf
        '''

        def __init__(self, square, points):
            '''
            Initialize this quadtree leaf
            '''
            super(QuadTree._QuadTreeLeaf, self).__init__(square)
            self._points = points[:]

        def __str__(self):
            '''
            Stringify this quadtree leaf
            '''
            return 'QuadTreeLeaf([%s])' % (','.join([str(point) for point in self._points]),)

        def _report_all_points(self):
            '''
            Report all points that lie in this leaf
            '''
            pass # A COMPLETER

        def _report_points_in_rectangle(self, rectangle):
            '''
            Report all points stored in this quadtree leaf that are
            in a query rectangle
            '''
            pass # A COMPLETER

    def __init__(self, points, granularity):
        '''
        Initialize this quadtree
        '''
        if granularity < 1:
            raise QuadTreeException('QuadtTree requieres a positive granularity')
        if points == []:
            self._root = None
        else:
            square = QuadTree._minimum_enclosing_square(points)
            self._root = QuadTree._construct_from_points(points, square, granularity)

    def __iter__(self):
        '''
        Return an iterator over all points stored in this quadtree
        '''
        return iter(self._root) if self._root is not None else iter([])

    def size(self):
        '''
        Return the number of points stored in this quadtree
        '''
        return self._root.size() if self._root is not None else 0

    def report_points_in_rectangle(self, rectangle):
        '''
        Return all points stored in this quadtree that are in the query rectangle
        '''
        return self._root._report_points_in_rectangle(rectangle) \
            if self._root is not None else []

    @staticmethod
    def _minimum_enclosing_square(points):
        '''
        Return the minimum square that contains the given points
        '''
        # x coordinate
        x_min = min(point.x for point in points)
        x_max = max(point.x for point in points)
        width = x_max - x_min
        # y coordinate
        y_min = min(point.y for point in points)
        y_max = max(point.y for point in points)
        height = x_max - x_min
        # contruct the minimum size square
        return Rectangle(Point(x_min, y_min),
                         Point(x_min + max(width, height), y_min + max(width, height)))

    @staticmethod
    def _construct_from_points(points, square, granularity):
        '''
        Construct a quadtree from a colection of points
        '''
        if len(points) <= granularity:
            return QuadTree._QuadTreeLeaf(square, points)

        else:
            # cut the square area into 4 square areas
            x_mid = square.lower_left_point.x + \
               ((square.upper_right_point.x - square.lower_left_point.x) / 2.0)
            y_mid = square.lower_left_point.y + \
                ((square.upper_right_point.y - square.lower_left_point.y) / 2.0)

            # upper right square area
            upper_right_square = Rectangle(Point(x_mid, y_mid),
                                           square.upper_right_point)
            points_in_upper_right_square = [point for point in points
                                            if point.x > x_mid and point.y > y_mid]
            upper_right = QuadTree._construct_from_points(points_in_upper_right_square,
                                                          upper_right_square,
                                                          granularity)

            # upper left square area
            upper_left_square = Rectangle(Point(square.lower_left_point.x, y_mid),
                                          Point(x_mid, square.upper_right_point.y))
            points_in_upper_left_square = [point for point in points
                                           if point.x <= x_mid and point.y > y_mid]
            upper_left = QuadTree._construct_from_points(points_in_upper_left_square,
                                                         upper_left_square,
                                                         granularity)

            # lower left square area
            lower_left_square = Rectangle(square.lower_left_point,
                                          Point(x_mid, y_mid))
            points_in_lower_left_square = [point for point in points
                                           if point.x <= x_mid and point.y <= y_mid]
            lower_left = QuadTree._construct_from_points(points_in_lower_left_square,
                                                         lower_left_square,
                                                         granularity)

            # lower right square area
            lower_right_square = Rectangle(Point(x_mid, square.lower_left_point.y),
                                           Point(square.upper_right_point.x, y_mid))
            points_in_lower_right_square = [point for point in points
                                            if point.x > x_mid and point.y <= y_mid]
            lower_right = QuadTree._construct_from_points(points_in_lower_right_square,
                                                          lower_right_square,
                                                          granularity)

        # done (leaf or recursive construction), construct and return the quadtree
        return QuadTree._QuadTreeInternalNode(square, upper_right, upper_left, lower_left, lower_right)


################################################################################
