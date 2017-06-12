#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common import Point_3D, Ball, combination_traversal
from scipy.optimize import fsolve

LOG_LEVEL = 0

def calculate_3d(length, balls, restrictions):
    def max_ball(restriction):
        # TODO:this should be saved in each restriction for less calculation
        # but I don't want to do this
        '''get max ball in each part'''
        def get_formulas(array):
            x, y, z, r = array
            ball = {
                'center': Point_3D({
                    'x': x,
                    'y': y,
                    'z': z,
                }),
                'radius':r
            }
            return list(map(lambda re: re.is_tangent_to(ball), restriction))

        if len(restriction) > 4:
            # for comparing
            the_max_ball = Ball({ 'x': 100, 'y': 100, 'z': 100}, 0)

            all_four_combinations = combination_traversal(restriction, 4)
            for combination in all_four_combinations:
                ball = max_ball(combination)
                all_valid = True
                for single_restriction in restriction:
                    valid = single_restriction.is_valid(ball)
                    if not valid:
                        if LOG_LEVEL > 0:
                            print(single_restriction.dictify(), valid, ball.dictify())
                        all_valid = False
                        break
                if ball.radius >= the_max_ball.radius and all_valid:
                    the_max_ball = ball
            return the_max_ball

        # if we have the previous ball, use its center as root point.
        # if not, use the default point.
        prev_ball = restriction[0]
        start_point_3D = [100, 100, 100, 100]
        if hasattr(prev_ball, 'center'):
            start_point_3D = [prev_ball.center.x, prev_ball.center.y, prev_ball.center.z, prev_ball.radius]

        x, y, z, r = fsolve(get_formulas, start_point_3D)

        return Ball({ 'x': x, 'y': y , 'z': z}, r)

    # loop end
    if len(balls) >= length:
        return balls, restrictions

    the_max_ball = max_ball(restrictions)
    balls.append(the_max_ball)

    # put the largest ball at [0]
    restrictions.insert(0, the_max_ball)

    return calculate_3d(length, balls, restrictions)

