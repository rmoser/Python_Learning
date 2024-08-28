# Advent of Code
year = 2023
day = 13

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
import utils

text0 = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
text1 = aocd.get_data(day=day, year=year)


def score(arr):
    result = 0
    for c in range(1, arr.shape[1]):
        w = min(c, arr.shape[1]-c)
        a = arr[:,c-w:c]
        b = arr[:, c:c+w]

        if np.all(a == b[:,::-1]):
            result += c

    for r in range(1, arr.shape[0]):
        h = min(r, arr.shape[0]-r)
        a = arr[r-h:r, :]
        b = arr[r:r+h, :]

        if np.all(a == b[::-1, :]):
            result += r * 100

    return result


def score2(arr):
    result = 0
    for c in range(1, arr.shape[1]):
        w = min(c, arr.shape[1]-c)
        a = arr[:,c-w:c]
        b = arr[:, c:c+w]

        m = a != b[:, ::-1]
        if m.sum() == 1:
            l = np.where(m)
            arr[l] = 1 - arr[l]
            return c

    for r in range(1, arr.shape[0]):
        h = min(r, arr.shape[0]-r)
        a = arr[r-h:r, :]
        b = arr[r:r+h, :]

        m = a != b[::-1, :]
        if m.sum() == 1:
            l = np.where(m)
            arr[l] = 1 - arr[l]
            return r * 100

    return result

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n')
    for i, t in enumerate(text):
        text[i] = np.array([list(t) for t in text[i].splitlines()])
        text[i] = (text[i] == '#').astype(int)

    pone = sum(score(t) for t in text)
    ptwo = sum(score2(t) for t in text)


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
