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
    return (arr.shape[0]-(np.where(arr==2)[0])).sum()

def load_cycle(n, mem, start, loop, shape):
    if n < start:
        t = mem[n]
    else:
        t = mem[start + (n-start)%loop]
    arr = np.array(t).reshape(shape)
    return calc_load(arr)

def north(arr):
    arr = arr.copy()
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
    _arr = arr.copy()
    for _ in range(4):
        _arr = north(_arr)
        _arr = np.rot90(_arr, -1)
    return _arr


utils.DEFAULT_TRANSLATE[ord('2')] = 'O'

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = np.array([list(x) for x in text.strip().splitlines()])
    arr = (text=='#') + (text=='O')*2
    arr = arr.astype(int)
    shape = arr.shape

    n_arr = north(arr)
    # utils.show(n_arr)
    pone = calc_load(north(arr))

    print(f"AOC {year} day {day}  Part One: {pone}")

    mem = dict()

    _arr = arr.copy()
    threshold = 1000
    for i in range(10**9):
        # print(i, calc_load(_arr))
        arg = tuple(_arr.flatten().tolist())

        if arg in mem.values():
            break

        mem[i] = arg
        _arr = mem_spin(arg, shape)

        print(f'\r{i}...', end='\t\t\t\t')
    print()

    end_iter = i
    start_iter = list(mem.values()).index(arg)
    loop_len = end_iter - start_iter

    ptwo = load_cycle(10**9, mem, start_iter, loop_len, shape)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
