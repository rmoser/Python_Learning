# Advent of Code
year = 2020
day = 15

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import pandas as pd

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """0,3,6"""
text0 = "1,3,2"
text1 = aocd.get_data(day=day, year=year)

def run(nums, stop):
    t = 0
    turns = dict()
    result = []
    while t < stop:
        t += 1
        if t <= len(nums):
            n = nums[t-1]  # Get from starting list
        else:
            n = newness  # Age of the last number spoken
        if n not in turns:
            newness = 0
        else:
            newness = t - turns[n]
        turns[n] = t
        result.append(n)
        # pprint(turns)
    return result

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = [int(x) for x in text.strip().split(',')]

    data = run(text, 30000000)
    pone = data[2020-1]
    ptwo = data[-1]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
