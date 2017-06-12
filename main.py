#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from sympy import *
# from sympy.core.symbol import symbols
# from sympy import Abs, sqrt, nsolve
# from sympy.solvers.solveset import nonlinsolve
from scipy.optimize import fsolve
# import sympy

NEARLY_ZERO = 0.001

LOG_LEVEL = 0
''' this is an example on what scipy can do

from scipy.optimize import fsolve

def func(i):
    x, y, z = i[0], i[1], i[2]
    return [
            x + 2 * y + 3 * z - 6,
            5 * (x ** 2) + 6 * (y ** 2) + 7 * (z ** 2) - 18,
            9 * (x ** 3) + 10 * (y ** 3) + 11 * (z ** 3) - 30
           ]
def main():
    r = fsolve(func,[0, 0, 0])
    print(r)
'''

class Restriction(object):
    """Restriction"""
    def __init__(self):
        super(Restriction, self).__init__()
    def is_valid(self, circle):
        return True

    def is_tangent_to(self, circle):
        return 0

    def dictify(self):
        return {}


class Point(Restriction):
    """Point"""
    def __init__(self, point):
        super(Point, self).__init__()
        self.x, self.y, self.z = point['x'], point['y'], point['z']

    def is_valid(self, circle):
        center, radius = circle.center, circle.radius
        return self.distant_to_pow(center.dictify()) - radius**2 > -NEARLY_ZERO

    def distant_to_pow(self, point):
        x, y, z = point['x'], point['y'], point['z']
        return (self.x - x) ** 2 + (self.y - y) ** 2 + (self.z - z) ** 2

    def is_tangent_to(self, circle):
        center, radius = circle['center'], circle['radius']
        return self.distant_to_pow(center.dictify()) - radius**2

    def dictify(self):
        return { 'x': self.x, 'y': self.y, 'z': self.z }

class Coordinate(Restriction):
    """Coordinate"""
    def __init__(self, attr, border, is_max=True):
        super(Coordinate, self).__init__()
        self.attr = attr
        self.border = border
        self.is_max = is_max
        # self.valid_point = Point(valid_point)

    def in_range(self, value):
        if self.is_max and value <= self.border:
            return True
        if not self.is_max and value >= self.border:
            return True
        return False
    def is_valid(self, circle):
        center, radius = circle.center, circle.radius
        return self.in_range(center.dictify()[self.attr]) and self.distant_to_pow(center.dictify()) - radius ** 2 > -NEARLY_ZERO
        # previous method
        # center, radius = circle.center, circle.radius
        # lx1, ly1, lx2, ly2 = self.begin.x, self.begin.y, self.end.x, self.end.y
        # x1, y1, x2, y2 = self.valid_point.x, self.valid_point.y, center.x, center.y
        # same_side = ((y1-y2)*(lx1-x1)+(x2-x1)*(ly1-y1))*((y1-y2)*(lx2-x1)+(x2-x1)*(ly2-y1)) >= -NEARLY_ZERO
        # if not same_side:
            # print('\n'
                    # , lx1, ly1, lx2,ly2
                    # , '\n'
                    # , x1, y1, x2, y2
                    # , '\n'
                    # , ((y1-y2)*(lx1-x1)+(x2-x1)*(ly1-y1))
                    # , '\n'
                    # , ((y1-y2)*(lx2-x1)+(x2-x1)*(ly2-y1))
                    # , '\n')
        # return self.distant_to_pow(center.dictify()) - radius**2 >= -NEARLY_ZERO and same_side

    def distant_to_pow(self, point):
        req_coordinate = point[self.attr]
        distant = abs(req_coordinate - self.border)
        return distant ** 2

    def is_tangent_to(self, circle):
        center, radius = circle['center'], circle['radius']
        return self.distant_to_pow(center.dictify()) - radius**2

    def dictify(self):
        return { 'attr': self.attr, 'border': self.border, 'is_max': self.is_max }

class Circle(Restriction):
    """Circle"""
    def __init__(self, center, radius):
        super(Circle, self).__init__()
        self.center = Point(center)
        self.radius = radius

    def is_valid(self, circle):
        center, radius = circle.center, circle.radius
        # if not abs(self.center.distant_to_pow(center.dictify()) - (radius + self.radius)**2) < NEARLY_ZERO:
            # print(self.center.distant_to_pow(center.dictify()))
            # print((radius + self.radius)**2)
        return self.center.distant_to_pow(center.dictify()) - (radius + self.radius)**2 > -NEARLY_ZERO

    def is_tangent_to(self, circle):
        center, radius = circle['center'], circle['radius']
        return self.center.distant_to_pow(center.dictify()) - (self.radius + radius)**2

    def dictify(self):
        return { 'center': self.center.dictify(), 'radius': self.radius }

# pick all 3-combination from all collections
def combination_traversal(combine_list, combine_num):
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

# print(combination_traversal([1,2,3,4,5], 3))

def calculate(length, circles, restrictions):
    def max_circle(restriction):
        # TODO:this should be saved in each restriction for less calculation
        # but I'm not saving restriction as an dict/object
        '''get max circle in each part'''
        def get_formulas(array):
            x, y, z, r = array
            circle = {
                'center': Point({
                    'x': x,
                    'y': y,
                    'z': z,
                }),
                'radius':r
            }
            return list(map(lambda re: re.is_tangent_to(circle), restriction))

        if len(restriction) > 4:
            the_max_circle = Circle({ 'x': 100, 'y': 100, 'z': 100}, 0)
            all_four_combinations = combination_traversal(restriction, 4)
            for combination in all_four_combinations:
                circle = max_circle(combination)
                all_valid = True
                for single_restriction in restriction:
                    valid = single_restriction.is_valid(circle)
                    if not valid:
                        if LOG_LEVEL > 0:
                            print(single_restriction.dictify(), valid, circle.dictify())
                        all_valid = False
                        break
                if circle.radius >= the_max_circle.radius and all_valid:
                    the_max_circle = circle
            return the_max_circle

        # set the prev circle's centre as root point
        prev_circle = restriction[0]
        start_point = [100, 100, 100, 100]
        if hasattr(prev_circle, 'center'):
            start_point = [prev_circle.center.x, prev_circle.center.y, prev_circle.center.z, prev_circle.radius]

        x, y, z, r = fsolve(get_formulas, start_point)

        return Circle({ 'x': x, 'y': y , 'z': z}, r)

    # end loop
    if len(circles) >= length:
        return circles, restrictions

    # put the largest on to [0]
    # restrictions.sort(key=lambda x: max_circle(x).radius)
    # restrictions.reverse()

    # new_restriction = restrictions[0]

    the_max_circle = max_circle(restrictions)
    circles.append(the_max_circle)

    # TODO: this can be optimized...but I don't want to this now...
    # new_restriction_list = [[j for j in new_restriction if j != i] for i in new_restriction]

    # add circle itself to restriction list
    # for restriction in new_restriction_list:
        # restriction.insert(0, the_max_circle)

    # remove the previous part
    # restrictions.pop(0)

    # new restrictions produced by new circle
    restrictions.append(the_max_circle)

    return calculate(length, circles, restrictions)




def main():
    circles = [
    ]
    restrictions = [
        Point({ 'x': 40, 'y': 100, 'z': 40 }),
        Coordinate('x', border=0, is_max=False),
        Coordinate('x', border=200, is_max=True),
        Coordinate('y', border=0, is_max=False),
        Coordinate('y', border=200, is_max=True),
        Coordinate('z', border=0, is_max=False),
        Coordinate('z', border=200, is_max=True),
    ]
    circles, restrictions = calculate(10, circles, restrictions)
    for circle in circles:
        # print(circle.center.distant_to_pow({ 'x': 40, 'y': 100, 'z': 40 }), circle.radius**2)
        print(circle.dictify())


if __name__ == "__main__":
    main()

