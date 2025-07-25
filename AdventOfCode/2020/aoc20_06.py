# Advent of Code
year = 2020
day = 6

import numpy as np
import aocd
import os
import itertools as it
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""
text1 = aocd.get_data(day=day, year=year)

def count_any(group):
    result = set()
    for c in group:
        if 97 <= ord(c) <= 122:
            result.add(c)
    return len(result)

def count_all(group):
    _group = group.split()
    result = set(_group[0])
    for c in _group[1:]:
        result &= set(c)
    return len(result)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n')

    pone = sum(count_any(g) for g in text)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = sum(count_all(g) for g in text)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
