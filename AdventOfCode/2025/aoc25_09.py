# Advent of Code
from scipy.spatial import distance_matrix

year = 2025
day = 9

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic
import itertools as it
import scipy as sp
import pandas as pd
import functools
from utils import RangeSet

text0 = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
text1 = aocd.get_data(day=day, year=year)

def valid_rectangle(a, b, data):
    rectangle = np.array([a, b])
    ul = rectangle.min(axis=0)
    lr = rectangle.max(axis=0)

    return data[ul[0]:lr[0]+1, ul[1]:lr[1]+1].all()

def rectangle_area(a, b):
    return abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)

if __name__ == '__main__':
    ic.disable()
    # ic.enable()

    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = np.array([[int(x) for x in line.split(',')] for line in text])
    _arr = np.expand_dims(arr, axis=2)
    dist = np.abs(_arr - _arr.T) + 1
    area = np.triu(dist.prod(axis=1))

    pone = area.max()
    print(f"AOC {year} day {day}  Part One: {pone}")


    img_size = arr.max()+2
    img = np.full((img_size, img_size), dtype=np.int8, fill_value=0)

    # Fill array for edges of shape
    for a, b in zip(arr, np.roll(arr, 1, axis=0)):
        ic(a, b)
        x = sorted((a[0], b[0]))
        y = sorted((a[1], b[1]))
        img[x[0]:x[1]+1, y[0]:y[1]+1] = 2
        img[*a] = 1
        img[*b] = 1


    new = sp.ndimage.binary_fill_holes(img)

    areas = np.unravel_index(area.argsort(axis=None), area.shape)
    areas = np.array(list(zip(*areas)))

    for a, b in reversed(areas):
        corner_a = arr[a]
        corner_b = arr[b]
        ic(f"Checking rectangle {corner_a} x {corner_b}...Area {area[a, b]}")

        if valid_rectangle(corner_a, corner_b, new):
            ic("Valid!")
            ptwo = area[a, b]
            break
        ic("Invalid!")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
