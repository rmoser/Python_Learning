# Advent of Code
year = 2023
day = 18

import numpy as np
import aocd
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
import utils
from pprint import pprint
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
import functools
from matplotlib import pyplot as plt

text0 = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
text1 = aocd.get_data(day=day, year=year)

def fill(pos, arr):
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
    to_fill = [pos]

    while to_fill:
        pos = to_fill.pop()
        if arr[pos] == 0:
            arr[pos] = 1
        for d in dirs:
            p = tuple(pos + np.array(d))
            if arr[p] == 0:
                to_fill.append(p)


def proc(steps):
    # calculate boundary dimensions
    dirs = {'R': np.array((0, 1)), 'D': np.array((1, 0)), 'L': np.array((0, -1)), 'U': np.array((-1, 0))}
    dirs[0] = dirs['R']
    dirs[1] = dirs['D']
    dirs[2] = dirs['L']
    dirs[3] = dirs['U']

    xy = np.zeros((len(steps), 2), dtype=int)
    for i, (d, n, c) in enumerate(steps):
        xy[i] = dirs[d] * n

    xyc = np.cumulative_sum(xy, axis=0)

    xy_min = xyc.min(axis=0)
    xy_max = xyc.max(axis=0)

    arr = np.zeros(shape=(xy_max-xy_min+(1,1)), dtype=bool)
    start = tuple(int(i) for i in -1 * xy_min)  # (0, 0) in coordinate system

    arr[start] = 1
    pos = start
    for step in xy:
        # i = 0
        # i += 1
        # step = xy[i]
        p = tuple(int(i) for i in pos + step)
        # print(step, pos, p)

        arr[min(pos[0], p[0]):max(pos[0], p[0]) + 1, min(pos[1], p[1]):max(pos[1], p[1]) + 1] = 1
        pos = p

    pos = tuple(np.array(np.where(arr)).mean(axis=1).astype(int))
    fill(pos, arr)

    return arr


def proc2(steps):
    # calculate boundary dimensions
    dirs = {'R': np.array((0, 1)), 'D': np.array((1, 0)), 'L': np.array((0, -1)), 'U': np.array((-1, 0))}
    dirs[0] = dirs['R']
    dirs[1] = dirs['D']
    dirs[2] = dirs['L']
    dirs[3] = dirs['U']

    xy = np.zeros((len(steps), 2), dtype=int)
    for i, (d, n, c) in enumerate(steps):
        xy[i] = dirs[d] * n

    xyc = np.cumulative_sum(xy, axis=0)

    x = np.unique(xyc[:, 1])
    y = np.unique(xyc[:, 0])

    @functools.cache
    def x_idx(val, x=x):
        if isinstance(val, int) and x.ndim == 1:
            return np.argwhere(x == val)[0,0]

        if isinstance(val, (tuple, np.array)) and x.ndim == 2:
            shape = x.shape
            return x[x * x.shape]

    @functools.cache
    def y_idx(val, y=y):
        return np.argwhere(y == val)[0,0]


    xy_min = xyc.min(axis=0)
    xy_max = xyc.max(axis=0)

    # REFACTOR: Memory inefficient
    # arr = np.zeros(shape=(xy_max-xy_min+(1,1)), dtype=bool)
    barr = np.zeros(shape=2 * np.array((len(x), len(y))) + 1, dtype=bool)  # Mask
    arr = np.ones_like(barr, dtype=int)  # Weights

    start = tuple(int(i) for i in -2 * xy_min)  # (0, 0) in coordinate system

    barr[start] = 1
    pos = start
    for step in xy:
        # i = 0
        # i += 1
        # step = xy[i]
        p = tuple(int(i) for i in pos + step * 2)
        # print(step, pos, p)

        barr[min(pos[0], p[0]):max(pos[0], p[0]) + 1, min(pos[1], p[1]):max(pos[1], p[1]) + 1] = 1
        pos = p

    pos = tuple(np.array(np.where(arr)).mean(axis=1).astype(int))
    fill(pos, arr)

    return arr, barr


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    steps = []
    for line in text.strip().splitlines():
        d, n, c = line.split()
        n = int(n)
        c = c[1:-1]
        steps.append((d, n, c))

    arr = proc(steps)

    # if text == text0:
    #     utils.show(arr)
    # else:
    #     plt.imshow(arr* 256)
    #     plt.show()

    pone = arr.sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    steps_2 = []
    for _, _, c in steps:
        # print(c)
        steps_2.append((int(c[-1]), int(c[1:-1], 16), ''))

    arr2 = proc(steps_2)
    ptwo = arr2.sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
