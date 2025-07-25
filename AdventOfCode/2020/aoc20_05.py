# Advent of Code
year = 2020
day = 5

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import math

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
FBFBBFFRLR
"""
text1 = aocd.get_data(day=day, year=year)

def parse(ticket):
    decode = {'F': '0', 'B': '1', 'R': '1', 'L': '0'}
    row_code = ''.join([decode[i] for i in ticket[:7]])
    col_code = ''.join([decode[i] for i in ticket[7:]])
    return int(row_code, 2), int(col_code, 2)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    ids = set()
    pone = 0
    for r, c in [parse(x) for x in text]:
        pone = max(pone, r*8+c)
        ids.add(r*8+c)

    print(f"AOC {year} day {day}  Part One: {pone}")

    # pos = np.where(arr == False)[0]
    # ptwo = pos[0] * 8 + pos[1]

    for a, b in it.pairwise(sorted(ids)):
        if b - a == 2:
            ptwo = b - 1
            break

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
