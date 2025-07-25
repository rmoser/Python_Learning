# Advent of Code
year = 2023
day = 21

import numpy as np
import aocd
import os
import utils
from pprint import pprint
import itertools as it
import math

utils.DEFAULT_TRANSLATE = {}

text0 = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n' if '\n\n' in text else '\n')
    arr = np.array([list(x) for x in text])
    start = tuple(np.array(np.where(arr=='S')).flatten().tolist())
    arr = (arr == '#').astype(int) * 99
    arr[arr==0] = -1
    arr[start] = 0

    utils.show(arr, start=start)

    _arr = arr.copy()
    pos_list = [start]
    for i in range(65):
        pos_list = list(map(tuple, np.array(np.where(_arr == i)).T.tolist()))

        for pos in pos_list:
            for direction in ((0,1), (0,-1), (1,0), (-1,0)):
                new_pos = np.array(pos) + direction
                if (new_pos < 0).any() or (new_pos >= _arr.shape).any():
                    continue
                new_pos = tuple(new_pos)
                if _arr[new_pos] < 0:
                    _arr[new_pos] = i+1

    utils.show(_arr, start=start)

    pone = (_arr % 2 == 0).sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
