# Advent of Code
year = 2023
day = 14

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
import utils
import functools

text0 = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
text1 = aocd.get_data(day=day, year=year)
translation = {ord('1'): ord('#'), ord('0'): ord('·'), ord('2'): ord('O')}


def calc_load(arr):
    return sum(arr.shape[0]-r for r in np.where(arr==2)[0])


def north(arr):
    rocks = zip(*np.where(arr == 2))

    for r, c in rocks:
        if not r:
            continue

        _r = r
        while _r and arr[_r-1, c] == 0:
            _r -= 1
        if _r != r:
            arr[_r, c] = arr[r, c]
            arr[r, c] = 0

    return arr


@functools.cache
def mem_spin(t, shape):
    a = np.array(t).reshape(shape)
    return spin(a)


def spin(arr):
    # utils.show(arr, translate=translation)
    _arr = north(arr.copy())
    _arr = np.rot90(_arr, axes=(1, 0))
    # utils.show(_arr, translate=translation)

    # West
    _arr = north(_arr)
    _arr = np.rot90(_arr, axes=(1, 0))
    # utils.show(_arr, translate=translation)

    # South
    _arr = north(_arr)
    _arr = np.rot90(_arr, axes=(1, 0))
    # utils.show(_arr, translate=translation)

    # East
    _arr = north(_arr)
    _arr = np.rot90(_arr, axes=(1, 0))
    # utils.show(_arr, translate=translation)

    return _arr


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = np.array([list(x) for x in text.strip().splitlines()])
    arr = (text=='#') + (text=='O')*2
    arr = arr.astype(int)
    shape = arr.shape

    # utils.show(arr, translate=translation)

    rocks = zip(*np.where(arr == 2))

    for r, c in rocks:
        if not r:
            continue

        _r = r
        while _r and arr[_r-1, c] == 0:
            _r -= 1
        if _r != r:
            # print('\n', r, c)
            arr[_r, c] = arr[r, c]
            arr[r, c] = 0

            # utils.show(arr, translate=translation)

    pone = calc_load(arr)

    print(f"AOC {year} day {day}  Part One: {pone}")

    for i in range(1000000000):
        _arr = mem_spin(tuple(arr.flatten()), shape)
        arr = _arr
        # if i < 1000 or not i % 1000:
        print(i, end='\r')

    ptwo = calc_load(arr)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
