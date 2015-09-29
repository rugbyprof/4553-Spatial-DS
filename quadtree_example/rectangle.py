################################################################################


class RectangleException(Exception):
    pass


################################################################################


class Rectangle(object):
    '''
    A axis-parallel rectangle class defined by a lower left point and an upper right point
    '''
    
    def __init__(self, lower_left_point, upper_right_point):
        '''
        Initialize a rectangle from lower left and upper right points
        '''
        if not upper_right_point.dominates(lower_left_point):
            raise RectangleException('Bad coordinates')
        self._lower_left_point = lower_left_point
        self._upper_right_point = upper_right_point

    def __str__(self):
        '''
        Stringify a rectangle
        '''
        return '%s(%s,%s)' % \
            (self.__class__.__name__,
             str(self._lower_left_point),
             str(self._upper_right_point))

    def __contains__(self, point):
        '''
        Return True iff a given point lies inside this rectangle
        '''
        pass # A COMPLETER
    
    def contains_rectangle(self, rectangle):
        '''
        Return True iff a given rectangle lies completely inside this rectangle
        '''
        pass # A COMPLETER

    def does_not_intersect_with_rectangle(self, rectangle):
        '''
        Return True iff a given rectangle does not intersect with this rectangle
        '''
        if self._lower_left_point.x > rectangle._upper_right_point.x:
            # This rectangle is strictly to the right of the given rectangle
            return True
        elif self._upper_right_point.x < rectangle._lower_left_point.x:
            # This rectangle is strictly to the left of the given rectangle
            return True
        elif self._upper_right_point.y < self._lower_left_point.y:
            # This rectangle is strictly below the given rectangle
            return True
        elif self._lower_left_point.y > self._upper_right_point.y:
            # This rectangle is strictly above the given rectangle
            return True
        # still here !?
        return False
    
    def intersects_with_rectangle(self, rectangle):
        '''
        Return True iff a given rectangle intersects with this rectangle
        '''
        return not self.does_not_intersect_with_rectangle(rectangle)
    
    def get_lower_left_point(self):
        '''
        Return the lower point of this rectangle
        '''
        return self._lower_left_point

    lower_left_point = property(get_lower_left_point, None, None,
                                'lower left point read only property')

    def get_upper_right_point(self):
        '''
        Return the upper right point of this rectangle
        '''
        return self._upper_right_point

    upper_right_point = property(get_upper_right_point, None, None,
                                 'upper right point read only property')

    def width(self):
        '''
        Return the width of this rectangle
        '''
        return self._upper_right_point.x - self._lower_left_point.x

    def height(self):
        '''
        Return the height of this rectangle
        '''
        return self._upper_right_point.y - self._lower_left_point.y

################################################################################
