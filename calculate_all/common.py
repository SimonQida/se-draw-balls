#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NEARLY_ZERO = 0.001

class Restriction(object):
    """
    Restriction.
    Actually this is unnecessary.
    There is no common things but method name.
    """
    def __init__(self):
        super(Restriction, self).__init__()

    def is_valid(self, point):
        return True

    def is_tangent_to(self, point):
        return 0

    def dictify(self):
        return {}

class Point(Restriction):
    """
    Point
    """
    def __init__(self, point):
        super(Point, self).__init__()
        self.x, self.y = point['x'], point['y']

    def is_valid(self, ball):
        center, radius = ball.center, ball.radius
        return self.distant_to_pow(center.dictify()) - radius**2 > -NEARLY_ZERO

    def distant_to_pow(self, point):
        x, y = point['x'], point['y']
        return (self.x - x) ** 2 + (self.y - y) ** 2

    def is_tangent_to(self, circle):
        center, radius = circle['center'], circle['radius']
        return self.distant_to_pow(center.dictify()) - radius**2

    def dictify(self):
        return { 'x': self.x, 'y': self.y }


class Point_2D(Point):
    """
    Point_2D
    """
    def __init__(self, point):
        super(Point_2D, self).__init__(point)
        self.x, self.y = point['x'], point['y']

    def distant_to_pow(self, point):
        x, y = point['x'], point['y']
        return (self.x - x) ** 2 + (self.y - y) ** 2

    def dictify(self):
        return { 'x': self.x, 'y': self.y }

class Point_3D(Point):
    """
    Point_3D
    """
    def __init__(self, point):
        super(Point_3D, self).__init__(point)
        self.x, self.y, self.z = point['x'], point['y'], point['z']

    def distant_to_pow(self, point):
        x, y, z = point['x'], point['y'], point['z']
        return (self.x - x) ** 2 + (self.y - y) ** 2 + (self.z - z) ** 2

    def dictify(self):
        return { 'x': self.x, 'y': self.y, 'z': self.z }

class Coordinate(Restriction):
    """
    Coordinate.
    Limit x, y, z, by (max||min) borders.
    Can be optimized by passing function as argument.
    """
    def __init__(self, attr, border, is_max=True):
        super(Coordinate, self).__init__()
        self.attr = attr
        self.border = border
        self.is_max = is_max

    def in_range(self, value):
        if self.is_max and value <= self.border:
            return True
        if not self.is_max and value >= self.border:
            return True
        return False

    def is_valid(self, ball):
        center, radius = ball.center, ball.radius
        in_range = self.in_range(center.dictify()[self.attr])
        in_distant = self.distant_to_pow(center.dictify()) - radius ** 2 > -NEARLY_ZERO
        return in_range and in_distant

    def distant_to_pow(self, point_3D):
        req_coordinate = point_3D[self.attr]
        distant = abs(req_coordinate - self.border)
        return distant ** 2

    def is_tangent_to(self, ball):
        center, radius = ball['center'], ball['radius']
        return self.distant_to_pow(center.dictify()) - radius**2

    def dictify(self):
        return { 'attr': self.attr, 'border': self.border, 'is_max': self.is_max }

class Round_Like(Restriction):
    def __init__(self, center, radius):
        super(Round_Like, self).__init__()
        self.center = Point(center)
        self.radius = radius

    def is_valid(self, circle):
        center, radius = circle.center, circle.radius
        return self.center.distant_to_pow(center.dictify()) - (radius + self.radius)**2 > -NEARLY_ZERO

    def is_tangent_to(self, ball):
        center, radius = ball['center'], ball['radius']
        return self.center.distant_to_pow(center.dictify()) - (self.radius + radius)**2

    def dictify(self):
        return { 'center': self.center.dictify(), 'radius': self.radius }

class Circle(Round_Like):
    """
    Circle
    """
    def __init__(self, center, radius):
        super(Circle, self).__init__(center, radius)
        self.center = Point_2D(center)

class Ball(Round_Like):
    """
    Ball
    """
    def __init__(self, center, radius):
        super(Ball, self).__init__(center, radius)
        self.center = Point_3D(center)

# pick all n-combination from all collections
def combination_traversal(combine_list, combine_num):
    # traversal end
    if len(combine_list) <= combine_num:
        return [combine_list]
    if combine_num == 0:
        return [[]]

    combinations = []

    comb_with_first = combination_traversal(combine_list[1:], combine_num - 1)

    for comb in comb_with_first:
        comb.insert(0, combine_list[0])

    combinations.extend(comb_with_first)

    comb_without_first = combination_traversal(combine_list[1:], combine_num)
    combinations.extend(comb_without_first)

    return combinations

