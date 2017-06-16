#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from common import Point_2D, Circle, combination_traversal
from scipy.optimize import fsolve

LOG_LEVEL = 0

def calculate_2d(length, circles, restrictions, real_time_callback=lambda x: x):
    def max_circle(restriction):
        # TODO:this should be saved in each restriction for less calculation
        # but I don't want to do this
        '''get max circle in each part'''
        def get_formulas(array):
            x, y, r = array
            circle = {
                'center': Point_2D({
                    'x': x,
                    'y': y,
                }),
                'radius':r
            }
            return list(map(lambda re: re.is_tangent_to(circle), restriction))

        if len(restriction) > 3:
            # for comparing
            the_max_circle = Circle({ 'x': 100, 'y': 100}, 0)

            all_four_combinations = combination_traversal(restriction, 3)
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

        # if we have the previous circle, use its center as root point.
        # if not, use the default point.
        prev_circle = restriction[0]
        start_point_2D = [100, 100, 100]
        if hasattr(prev_circle, 'center'):
            start_point_2D = [prev_circle.center.x, prev_circle.center.y, prev_circle.radius]

        x, y, r = fsolve(get_formulas, start_point_2D)

        return Circle({ 'x': x, 'y': y}, r)

    # loop end
    if len(circles) >= length:
        return circles, restrictions

    the_max_circle = max_circle(restrictions)
    real_time_callback(the_max_circle)
    circles.append(the_max_circle)

    # put the largest circle at [0]
    restrictions.insert(0, the_max_circle)

    return calculate_2d(length, circles, restrictions, real_time_callback)

