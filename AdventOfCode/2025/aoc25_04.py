# Advent of Code
year = 2025
day = 4

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic

text0 = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = (np.array([[c for c in line] for line in text]) == '@').astype(int)

    sums = utils.sum_neighbors(arr)
    pone = (sums[np.where(arr)] < 4).sum()

    print(f"AOC {year} day {day}  Part One: {pone}")


    _arr = arr.copy()

    while (sums[np.where(_arr)] < 4).any():
        _arr[np.where(sums<4)] = 0
        sums = utils.sum_neighbors(_arr)
        # ic(_arr, sums)

    ptwo = arr.sum() - _arr.sum()

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
