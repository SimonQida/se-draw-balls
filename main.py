#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common import Point_2D, Point_3D, Circle, Ball, Coordinate, combination_traversal
from calculate_2d import calculate_2d
from calculate_3d import calculate_3d

def main():
    """
    example on how all these work
    """
    balls = []
    restrictions_3d = [
        Point_3D({ 'x': 40, 'y': 100, 'z': 40 }),
        Coordinate('x', border=0, is_max=False),
        Coordinate('x', border=200, is_max=True),
        Coordinate('y', border=0, is_max=False),
        Coordinate('y', border=200, is_max=True),
        Coordinate('z', border=0, is_max=False),
        Coordinate('z', border=200, is_max=True),
    ]
    balls, restrictions = calculate_3d(12, balls, restrictions_3d)
    for ball in balls:
        # print(ball.center.distant_to_pow({ 'x': 40, 'y': 100, 'z': 40 }), ball.radius**2)
        print(ball.dictify())

    print()
    restrictions_2d = [
        Point_2D({ 'x': 40, 'y': 100 }),
        Coordinate('x', border=0, is_max=False),
        Coordinate('x', border=200, is_max=True),
        Coordinate('y', border=0, is_max=False),
        Coordinate('y', border=200, is_max=True),
    ]
    circles = []
    circles, restrictions = calculate_2d(12, circles, restrictions_2d)
    for circle in circles:
        # print(ball.center.distant_to_pow({ 'x': 40, 'y': 100, 'z': 40 }), ball.radius**2)
        print(circle.dictify())

if __name__ == "__main__":
    main()

