# Advent of Code
year = 2020
day = 11

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import functools

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""
text1 = aocd.get_data(day=day, year=year)

def run(array):
    _arr = (array[:-2, :-2] == 1).astype(int)
    _arr += (array[1:-1, :-2] == 1)
    _arr += (array[2:, :-2] == 1)

    _arr += (array[:-2, 1:-1] == 1)
    _arr += (array[2:, 1:-1] == 1)

    _arr += (array[:-2, 2:] == 1)
    _arr += (array[1:-1, 2:] == 1)
    _arr += (array[2:, 2:] == 1)

    array[1:-1, 1:-1][np.bitwise_and(_arr==0, array[1:-1, 1:-1] <= 1)] = 1
    array[1:-1, 1:-1][np.bitwise_and(_arr>=4, array[1:-1, 1:-1] <= 1)] = 0

@functools.cache
def seats():
    return [tuple(x) for x in np.array(np.where(ARR != 9)).T.tolist()]

def run2():
    _arr = ARR.copy()
    for pos in seats():
        s = (ARR[nearest_seats(pos)]).sum()
        if s == 0:
            _arr[pos] = 1
        elif s >= 5:
            _arr[pos] = 0
    ARR[::] = _arr


ARR = None

@functools.cache
def valid(pos):
    return (0 <= pos[0] < ARR.shape[0]) and (0 <= pos[1] < ARR.shape[1])

@functools.cache
def nearest_seats(pos):
    result = []
    for dir in ([0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]):
        _pos = pos
        dir = np.array(dir)
        while _pos == pos or valid(_pos) and ARR[_pos] == 9:  # Skip empty tiles
            _pos = tuple((_pos + dir).tolist())
        if valid(_pos):
            result.append(_pos)
    return tuple(np.array(result).T)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    array = np.full(shape=(len(text)+2, len(text[0])+2), fill_value=9)
    array[1:-1, 1:-1] = 9 * (np.array([list(x) for x in text]) == '.')
    ARR = array[1:-1, 1:-1].copy()

    utils.DEFAULT_TRANSLATE = {ord('0'): 'L', ord('1'): '#', ord('9'): '.'}

    utils.show(array)

    _arr_copy = np.zeros_like(array)
    i = 0
    while True:
        i += 1
        _arr_copy[::] = array
        run(array)
        if (array == _arr_copy).all():
            break

    utils.show(array)

    pone = (array == 1).sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    i = 0
    _arr_copy = np.zeros_like(ARR)
    while True:
        i += 1
        _arr_copy[::] = ARR
        run2()
        if (ARR == _arr_copy).all():
            break


    ptwo = (ARR == 1).sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
