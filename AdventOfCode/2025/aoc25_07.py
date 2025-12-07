# Advent of Code
year = 2025
day = 7

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic

text0 = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
text1 = aocd.get_data(day=day, year=year)

def tachyon(arr):
    r = 0
    tachyons = list(np.where(arr[r]=='S')[0])
    splits = 0

    while True:
        r += 1
        if r == arr.shape[0]:
            return splits

        _tachyons = set()
        for t in tachyons:
            if arr[r,t] == '^':
                splits += 1
                if t > 0:
                    _tachyons.add(t-1)
                if t < len(arr)-1:
                    _tachyons.add(t+1)
            else:
                _tachyons.add(t)
            tachyons = list(_tachyons)


def timeline(arr):
    r = 0
    timelines = {list(arr[r]).index('S'): 1}

    while True:
        r += 1
        if r == arr.shape[0]:
            return sum(timelines.values())

        _timelines = timelines.copy()
        for t, v in timelines.items():
            if arr[r,t] == '^':
                _timelines[t] = 0
                if t > 0:
                    _timelines[t-1] = _timelines.get(t-1, 0) + v
                if t < len(arr)-1:
                    _timelines[t+1] = _timelines.get(t+1, 0) + v
            timelines = _timelines



if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = utils.map_from_text(text)
    pone = tachyon(arr)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = timeline(arr)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
