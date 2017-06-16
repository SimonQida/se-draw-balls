#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from calculate_all.common import Point_2D, Point_3D, Circle, Ball, Coordinate, combination_traversal
from calculate_all.calculate_2d import calculate_2d
from calculate_all.calculate_3d import calculate_3d
import turtle
import json

def main():
    """
    example on how all these work
    """

    balls = []
    restrictions_3d = [
        Point_3D({ 'x': 100, 'y': 80, 'z': 40 }),
        Point_3D({ 'x': 130, 'y': 100, 'z': 80 }),
        Coordinate('x', border=0, is_max=False),
        Coordinate('x', border=200, is_max=True),
        Coordinate('y', border=0, is_max=False),
        Coordinate('y', border=200, is_max=True),
        Coordinate('z', border=0, is_max=False),
        Coordinate('z', border=200, is_max=True),
    ]
    def print_dictified(ele): print(ele.dictify())
    # print can't put in lambda anymore in python2
    balls, restrictions = calculate_3d(20, balls, restrictions_3d, real_time_callback=print_dictified)

    exportToJson([ball.dictify() for ball in balls], './json-exports/3d.json')

    circles = []
    restrictions_2d = [
        Point_2D({ 'x': 40, 'y': 100 }),
        Coordinate('x', border=0, is_max=False),
        Coordinate('x', border=200, is_max=True),
        Coordinate('y', border=0, is_max=False),
        Coordinate('y', border=200, is_max=True),
    ]
    circles, restrictions = calculate_2d(12, circles, restrictions_2d, real_time_callback=print_dictified)
    # draw 2d circles
    # plot(circles)


def exportToJson(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
def plot(result):
    turtle.penup()
    turtle.goto(0, 300)
    turtle.pendown()
    turtle.forward(300)
    turtle.right(90)
    turtle.forward(300)
    turtle.right(90)
    turtle.forward(300)
    turtle.right(90)
    turtle.forward(300)
    turtle.right(90)
    turtle.penup()
    for item in result:
        turtle.penup()
        turtle.goto(item.center.x*1.5, (item.center.y-item.radius)*1.5)
        turtle.pendown()
        turtle.circle(item.radius*1.5)
    turtle.exitonclick()
if __name__ == "__main__":
    main()

