# Advent of Code
year = 2020
day = 9

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    if text == text0:
        preamble = 5
    else:
        preamble = 25

    text = text.strip().splitlines()
    arr = [int(x) for x in text]
    # print(arr)


    for i in range(preamble, len(arr)):
        # print(i, arr[i], arr[i-preamble:i])
        if not any(arr[i] == sum(x) for x in it.combinations(arr[i-preamble:i], 2)):
            pone = arr[i]
            break

    acc = np.zeros(shape=(len(arr), len(arr)), dtype=int)
    acc[0] = np.cumsum(arr)
    for i in range(1, len(arr)):
        acc[i][i:] = acc[i-1][i:] - acc[i-1][i-1]

    match = [x for x in zip(*np.where(acc == pone)) if x[0] != x[1]][0]

    nums = arr[match[0]:match[1]+1]

    ptwo = min(nums) + max(nums)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
