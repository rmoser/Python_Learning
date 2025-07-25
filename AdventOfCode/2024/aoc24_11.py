# Advent of Code
year = 2024
day = 11

import numpy as np
import aocd
import os
from functools import cache
from pprint import pprint
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """125 17"""
text1 = aocd.get_data(day=day, year=year)

@cache
def blink(s):
    if s == 0:
        return [1]

    if len(str(s)) % 2 == 0:
        stone = str(s)
        l = len(stone) // 2
        return [int(stone[:l]), int(stone[l:])]

    return [s * 2024]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split()

    d = dict()
    for i in [int(c) for c in text]:
        d[i] = d.get(i, 0) + 1

    # pprint(d)

    # print(stones)
    for j in range(25):
        for v, n in d.copy().items():
            if n == 0:
                continue
            d[v] = d.get(v, 0) - n
            for i in blink(v):
                # if v == 72:
                #     print(v, i, n, d[i])
                d[i] = d.get(i, 0) + n
        # print(j)
    # pprint([(k, v) for k, v in d.items() if v > 0])

    # print(len(stones))

    pone = sum(d.values())
    print(f"AOC {year} day {day}  Part One: {pone}")

    for j in range(50):
        for v, n in d.copy().items():
            if n == 0:
                continue
            d[v] = d.get(v, 0) - n
            for i in blink(v):
                # if v == 72:
                #     print(v, i, n, d[i])
                d[i] = d.get(i, 0) + n

    ptwo = sum(d.values())
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
