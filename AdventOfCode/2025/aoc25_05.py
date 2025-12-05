from __future__ import annotations

# Advent of Code
year = 2025
day = 5

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic
from utils import RangeSet

text0 = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    values = []
    mode = 0
    my_set = None
    for line in text:
        if not line:
            mode = 1
            continue

        if not mode:
            lo, hi = (int(x) for x in line.split('-'))
            if not my_set:
                my_set = RangeSet(lo, hi)
            else:
                my_set |= RangeSet(lo, hi)

        else:
            values.append(int(line))


    pone = sum(value in my_set for value in values)
    ptwo = len(my_set)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
