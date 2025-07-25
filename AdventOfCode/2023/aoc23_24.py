# Advent of Code
year = 2023
day = 24

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
import itertools as it
import scipy as sp

text0 = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()
    if text == text0:
        min_max = (7, 27)
    else:
        min_max = (200000000000000, 400000000000000)

    stones = []
    for line in text:
        pos, vel = line.split('@')
        x, y, z =  (int(c) for c in pos.split(','))
        dx, dy, dz =  (int(c) for c in vel.split(','))
        stones.append((x, y, z, dx, dy, dz))

    xy = np.zeros(shape=(len(stones) * (len(stones)-1) // 2, 4), dtype=float)
    xyz = np.zeros(shape=(len(stones) * (len(stones)-1) // 2, 6), dtype=float)
    # xyz_a = np.zeros(shape=(len(stones) * (len(stones)-1) // 2, 4), dtype=float)
    # xyz_b = np.zeros(shape=(len(stones), 1), dtype=float)

    for i, (a, b) in enumerate(it.combinations(stones, 2)):
        # print(i, a, b)
        xy_a = np.array([[a[4], -a[3], 0, 0], [b[4], -b[3], 0, 0], [1, 0, -a[3], 0], [0, 1, 0, -b[4]]])
        xy_b = np.array([[a[0] * a[4] - a[1] * a[3]], [b[0]*b[4]-b[1]*b[3]], [a[0]], [b[1]]])

        try:
            xy[i] = sp.linalg.solve(xy_a, xy_b).T
        except np.linalg.LinAlgError:
            xy[i] = np.repeat(np.inf, xy.shape[1])

    pone = np.bitwise_and(((min_max[0], min_max[0], 0, 0) <= xy), (xy <= (min_max[1], min_max[1], np.inf, np.inf))).all(axis=1).sum()


    A = [[], [], []]
    B = [[], [], []]

    z = list(np.zeros(shape=len(stones)))
    for i, s in enumerate(stones):
        _a = [1] + z.copy()
        _a[i+1] = -s[3]
        A[0].append(_a)
        B[0].append(s[0])

        _a = [1] + z.copy()
        _a[i+1] = -s[4]
        A[1].append(_a)
        B[1].append(s[1])

        _a = [1] + z.copy()
        _a[i+1] = -s[5]
        A[2].append(_a)
        B[2].append(s[2])

    A[0].append([0] + z.copy())
    A[1].append([0] + z.copy())
    A[2].append([0] + z.copy())
    B[0].append(0)
    B[1].append(0)
    B[2].append(0)

    A = np.array(A)
    B = np.array(B)
    sp.linalg.solve(A[0], B[0])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
