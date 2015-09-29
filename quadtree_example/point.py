################################################################################

import random

################################################################################

class Point(object):
    '''
    A simple 2D point class
    '''
    
    def __init__(self, x = 0, y = 0):
        '''
        Initialize a point with a and y coordinates
        '''
        self._x = x
        self._y = y

    def __eq__(self, point):
        '''
        Return True iff this point and the other point have the same coordinates
        '''
        return (self._x == point._x and self._y == point._y)

    def __str__(self):
        '''
        Stringify this point
        '''
        return '%s(%f,%f)' % (self.__class__.__name__, self._x, self._y)

    def get_x(self):
        '''
        Return the x coordinate of this point
        '''
        return self._x

    x = property(get_x, None, None, 'x coordinate read only property')

    def get_y(self):
        '''
        Return the y coordinate of this point
        '''
        return self._y

    y = property(get_y, None, None, 'y coordinate read only property')

    def dominates(self, point):
        '''
        Return True iff this point dominates the given point
        '''
        return self._x > point._x and self._y > point.y
    
################################################################################

class RandomPointGenerator(object):
    '''
    A convenient class to generate random points in a rectangle
    '''
    
    def __init__(self, rectangle):
        '''
        Initialize the generator with a rectangle
        '''
        self._rectangle = rectangle

    def __iter__(self):
        return self()

    def __call__(self):
        '''
        The generator by itself
        '''
        while True:
            x_rand = self._rectangle.lower_left_point.x + \
                (self._rectangle.width() * random.random())
            y_rand = self._rectangle.lower_left_point.y + \
                (self._rectangle.height() * random.random())
            yield Point(x_rand, y_rand)
        
################################################################################
