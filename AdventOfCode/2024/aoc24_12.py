# Advent of Code
year = 2024
day = 12

import numpy as np
import aocd
import os
import utils
import scipy as sp

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
text1 = aocd.get_data(day=day, year=year)

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def in_array(pos, arr):
    p = np.array(pos)
    return (p >= 0).all() and (p < arr.shape).all()

def perimeter(coords):
    result = 0
    for pos in coords:
        for d in DIRS:
            new_pos = tuple(pos + np.array(d))
            # result += not in_array(new_pos, arr) or new_pos not in coords
            result += new_pos not in coords
    return result


def perimeter2(coords):
    return perimeter2_up_down(coords) + perimeter2_up_down(sorted([(y, x) for x, y in coords]))

def perimeter2_up_down(coords):
    result = 0

    # Count north side fences
    new_fence = True
    for pos in coords:
        left_pos = (pos[0], pos[1] - 1)
        north_pos = (pos[0] - 1, pos[1])
        if north_pos not in coords:
            if left_pos not in coords or new_fence:
                new_fence = False
                result += 1
        else:
            new_fence = True

    # print(result)
    # Count south side fences
    new_fence = True
    for pos in coords:
        left_pos = (pos[0], pos[1] - 1)
        south_pos = (pos[0] + 1, pos[1])
        if south_pos not in coords:
            if left_pos not in coords or new_fence:
                new_fence = False
                # print(pos, south_pos, left_pos)
                result += 1
        else:
            new_fence = True
    # print(result)

    return result


def get_coords(symbol, arr):
    return [tuple(x) for x in np.array(np.where(arr == symbol)).transpose().tolist()]

if __name__ == '__main__':
    pone = 0
    ptwo = 0

    text = text1
    text = text.strip().splitlines()

    array = np.array([list(x) for x in text])
    # utils.show(array)
    # array_int = np.array(list(map(ord, array.flatten()))).reshape(array.shape)

    for symbol in np.unique(array):
        areas = sp.ndimage.label(array == symbol)
        for i in range(areas[1], 0, -1):
            shape = get_coords(i, areas[0])
            a = len(shape)
            p = perimeter(shape)
            # print(symbol, i, a, p, a*p)
            pone += a * p

            p2 = perimeter2(shape)

            # print(symbol, a, p2)
            ptwo += a * p2

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
