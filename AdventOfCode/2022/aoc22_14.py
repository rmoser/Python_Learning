# Advent of Code
year = 2022
day = 14

import numpy as np
import aocd
import itertools
import utils
import os
import time

text0 = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
text1 = aocd.get_data(day=day, year=year)


def show(arrmap):
    nonzero = np.where(arrmap > 0)
    rng = (nonzero[0].min(), nonzero[0].max()), (0, nonzero[1].max()+1)
    _arr = arrmap[rng[0][0]:rng[0][1] + 1, rng[1][0]:rng[1][1] + 1]
    utils.show(_arr.T, translate={ord('1'): ord('#'), ord('0'): ord('·'), ord('2'): ord('+'), ord('3'): ord('O')})


def run(map):
    arr = map.copy()
    pos = [x[0] for x in np.where(arr == 2)]

    turn = 0
    while True:
        try:
            new = [pos[0], pos[1]+1]
            if arr[tuple(new)] == 0:
                pos = new
                continue

            new = [pos[0]-1, pos[1]+1]
            if arr[tuple(new)] == 0:
                pos = new
                continue

            new = [pos[0]+1, pos[1]+1]
            if arr[tuple(new)] == 0:
                pos = new
                continue

        except IndexError:
            break

        if pos == source:
            arr[tuple(pos)] = 3
            break

        turn += 1
        arr[tuple(pos)] = 3
        pos = source.copy()

    return arr


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    for i, line in enumerate(text):
        text[i] = [tuple(int(x) for x in pair.split(',')) for pair in line.split(' -> ')]

    coords = np.array(list(itertools.chain.from_iterable(text)))
    xmin = coords[:, 0].min()
    xmax = coords[:, 0].max()
    ymax = coords[:, 1].max()+1

    source = [500, 0]
    rng = ((xmin, xmax), (0, ymax))

    arr = np.zeros(dtype=int, shape=(1000, ymax))
    arr[tuple(source)] = 2

    for line in text:
        for c0, c1 in zip(line[:-1], line[1:]):
            # print(c0, c1)
            x_rng = sorted([c0[0], c1[0]])
            y_rng = sorted([c0[1], c1[1]])
            for x in np.arange(x_rng[0], x_rng[1]+1):
                for y in np.arange(y_rng[0], y_rng[1]+1):
                    # print(x, y)
                    arr[x, y] = 1

    arr_pone = np.zeros(dtype=int, shape=(1000, ymax))
    arr_pone = arr

    arr_ptwo = np.zeros(dtype=int, shape=(1000, ymax+2))
    arr_ptwo[:, :ymax] = arr
    arr_ptwo[:, ymax+1] = 1

    arr_pone = run(arr_pone)
    pone = (arr_pone == 3).sum()


    arr_ptwo = run(arr_ptwo)
    ptwo = (arr_ptwo == 3).sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
