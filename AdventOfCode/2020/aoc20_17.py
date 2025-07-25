# Advent of Code
year = 2020
day = 17

import numpy as np
import scipy as sp
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
.#.
..#
###
"""
text1 = aocd.get_data(day=day, year=year)

def expand(array, n=None):
    if not n:
        n = array.ndim
    while array.ndim < n:
        array = np.expand_dims(array, axis=0)

    s = np.array(array.shape)

    _arr = np.zeros(shape=s+2, dtype=array.dtype)
    base_slice = (slice(1, -1, None), ) * _arr.ndim
    _arr[base_slice] = array

    return _arr

def reduce(array):
    nz = array.nonzero()
    r = tuple(slice(min(j), max(j)+1) for j in nz)
    return array[r]

# def run(arr):
#     arr = expand(expand(arr))
#     base = arr[1:-1, 1:-1, 1:-1]
#     neighbors = arr[:-2, 1:-1, 1:-1] + arr[1:-1, :-2, 1:-1] + arr[1:-1, 1:-1, :-2]
#     neighbors += arr[:-2, 2:, 2:] + arr[2:, :-2, 2:] + arr[2:, 2:, :-2]
#     neighbors += arr[:-2, :-2, 1:-1] + arr[1:-1, :-2, :-2] + arr[:-2, 1:-1, :-2]
#     neighbors += arr[:-2, :-2, 2:] + arr[2:, :-2, :-2] + arr[:-2, 2:, :-2]
#     neighbors += arr[1:-1, 1:-1, 2:] + arr[2:, 1:-1, 1:-1] + arr[1:-1, 2:, 1:-1]
#     neighbors += arr[1:-1, 2:, 2:] + arr[2:, 1:-1, 2:] + arr[2:, 2:, 1:-1]
#
#     neighbors += arr[:-2, :-2, :-2]
#     neighbors += arr[2:, 2:, 2:]
#
#     neighbors += arr[2:, 1:-1, :-2] + arr[2:, :-2, 1:-1]
#     neighbors += arr[1:-1, 2:, :-2] + arr[1:-1, :-2, 2:]
#     neighbors += arr[:-2, 1:-1, 2:] + arr[:-2, 2:, 1:-1]
#
#     return reduce(np.bitwise_and(base, np.bitwise_or(neighbors == 2, neighbors == 3)) + np.bitwise_and(np.bitwise_not(base), neighbors == 3))

def run(arr, n=3):
    arr = expand(arr, n)
    base = arr.copy()
    kernel = np.ones(shape = (3, ) * arr.ndim, dtype=int)
    center = tuple(np.array(kernel.shape) // 2)
    kernel[center] = 0

    neighbors = reduce(sp.signal.convolve(arr, kernel))
    return reduce(np.bitwise_and(base, np.bitwise_or(neighbors == 2, neighbors == 3)) + np.bitwise_and(np.bitwise_not(base), neighbors == 3))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    array = np.array(np.array([list(line) for line in text]) == '#', dtype=int)
    _arr1 = array.copy()
    _arr2 = array.copy()

    for _ in range(6):
        _arr1 = run(_arr1, 3)
        _arr2 = run(_arr2, 4)

    pone = _arr1.sum()
    ptwo = _arr2.sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
