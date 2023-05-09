# Advent of Code
year = 2018
day = 18

import numpy as np
import aocd
import itertools
import utils

text0 = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""
text1 = aocd.get_data(day=day, year=year)

Adj = np.array([(0, 1), (0, -1), (1, 0), (1, -1), (1, 1), (-1, -1), (-1, 0), (-1, 1)])


def run(arr, n=1):
    _arr = np.zeros(shape=np.array(arr.shape) + 2, dtype=arr.dtype)
    _arr[1:-1, 1:-1] = arr

    for i in range(n):
        _new_trees = (
            (_arr[1:-1, 1:-1] == 0) *  # Field rule
            ((
                (_arr[:-2, :-2] == 1).astype(int) + (_arr[:-2, 1:-1] == 1).astype(int) + (_arr[:-2, 2:] == 1).astype(int) +
                (_arr[1:-1, :-2] == 1).astype(int) + (_arr[1:-1, 2:] == 1).astype(int) +
                (_arr[2:, :-2] == 1).astype(int) + (_arr[2:, 1:-1] == 1).astype(int) + (_arr[2:, 2:] == 1).astype(int)
            ) >= 3)
        )
        _new_lumberyards = (
            (_arr[1:-1, 1:-1] == 1) *  # Tree rule
            ((
                 (_arr[:-2, :-2] == 2).astype(int) + (_arr[:-2, 1:-1] == 2).astype(int) + (_arr[:-2, 2:] == 2).astype(int) +
                 (_arr[1:-1, :-2] == 2).astype(int) + (_arr[1:-1, 2:] == 2).astype(int) +
                 (_arr[2:, :-2] == 2).astype(int) + (_arr[2:, 1:-1] == 2).astype(int) + (_arr[2:, 2:] == 2).astype(int)
            ) >= 3)
        )

        _new_fields = (
            (_arr[1:-1, 1:-1] == 2) *  # Lumberyard rule
            (np.bitwise_not(
                np.bitwise_and((
                    (_arr[:-2, :-2] == 1) + (_arr[:-2, 1:-1] == 1) + (_arr[:-2, 2:] == 1) +
                    (_arr[1:-1, :-2] == 1) + (_arr[1:-1, 2:] == 1) +
                    (_arr[2:, :-2] == 1) + (_arr[2:, 1:-1] == 1) + (_arr[2:, 2:] == 1)
                ),
                (
                    (_arr[:-2, :-2] == 2) + (_arr[:-2, 1:-1] == 2) + (_arr[:-2, 2:] == 2) +
                    (_arr[1:-1, :-2] == 2) + (_arr[1:-1, 2:] == 2) +
                    (_arr[2:, :-2] == 2) + (_arr[2:, 1:-1] == 2) + (_arr[2:, 2:] == 2)
                ))
            ))
        )

        # _new = _arr.copy()
        _arr[1:-1, 1:-1][_new_fields] = 0
        _arr[1:-1, 1:-1][_new_trees] = 1
        _arr[1:-1, 1:-1][_new_lumberyards] = 2

        if i % 1000000 == 0:
            print(f'\r{i}', end='')
        # _arr = _arr.copy()
        # for y in range(_arr.shape[0]):
        #     for x in range(_arr.shape[1]):
        #         _new[y, x] = check(_arr, (y, x))
        # _arr[1:-1, 1:-1] = _new[1:-1, 1:-1]

    print()
    return _arr[1:-1, 1:-1]


def check(arr, c):
    y, x = c
    subarr = arr[max(0, y - 1):min(arr.shape[0], y + 2), max(0, x - 1):min(arr.shape[1], x + 2)].copy()
    subarr[min(y, 1), min(x, 1)] = -1
    # show(subarr)
    if arr[y, x] == 0:
        if (subarr == 1).sum() >= 3:
            return 1
    elif arr[y, x] == 1:
        if (subarr == 2).sum() >= 3:
            return 2
    elif arr[y, x] == 2:
        if not (1 in subarr and 2 in subarr):
            return 0
    return arr[c]


def show(arr):
    _arr = arr[1] + arr[2]*2
    utils.show(_arr.astype(str), translate={ord('0'): ord('.'), ord('1'): ord('|'), ord('2'): ord('#')})


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.strip('\n').splitlines()

    tarr = np.array([list(x) for x in text])
    tarr = (tarr == '|') + (tarr == '#')*2

    arr = np.zeros(shape=(3, ) + tarr.shape , dtype=bool)
    arr[0] = tarr == 0
    arr[1] = tarr == 1
    arr[2] = tarr == 2

    arr10 = run(arr, 10)
    pone = (arr10 == 1).sum() * (arr10 == 2).sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    arr1000000000 = run(arr, 1000000000)
    ptwo = (arr1000000000 == 1).sum() * (arr1000000000 == 2).sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
