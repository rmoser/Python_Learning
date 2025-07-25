# Advent of Code
year = 2020
day = 1

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
1721
979
366
299
675
1456
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    nums = [int(x) for x in text]

    for a, b in it.combinations(nums, 2):
        if a + b == 2020:
            pone = a * b
            break

    for a, b, c in it.combinations(nums, 3):
        if a + b + c == 2020:
            ptwo = a * b * c
            break

    print(nums, a, b)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
