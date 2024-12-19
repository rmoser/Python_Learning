# Advent of Code
year = 2024
day = 2

import numpy as np
import aocd
import os
import itertools as it
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
text1 = aocd.get_data(day=day, year=year)

def check(arr):
    rep = list(zip(arr[:-1], arr[1:]))
    delta = np.array([a - b for a, b in rep])

    if (delta > 0).all() and np.bitwise_and(1 <= delta, delta <= 3).all():
        return 1
    if (delta < 0).all() and np.bitwise_and(-3 <= delta, delta <= -1).all():
        return 1
    return 0


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone = 0
    ptwo = 0
    for line in text:
        line = [int(x) for x in line.split()]

        res = check(line)
        pone += res

        if not res:
            for i in range(len(line)):
                d = np.append(line[:i], line[i+1:])

                res = check(d)
                if res:
                   break
        ptwo += res

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
