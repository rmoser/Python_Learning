# Advent of Code
year = 2024
day = 25

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    locks = []
    keys = []

    for lines in text.split('\n\n'):
        arr = np.array([list(line) for line in lines.splitlines()])
        arr = (arr == '#').astype(int)
        if arr[0].all():
            locks.append(arr.sum(axis=0)-1)
        else:
            keys.append(arr.sum(axis=0)-1)

    matches = []
    for k in keys:
        for l in locks:
            kl = k + l
            # print(l, k, kl)
            if (kl <= 5).all():
                matches.append((tuple(l.tolist()), tuple(k.tolist())))

    pone = len(matches)
    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
