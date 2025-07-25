# Advent of Code
year = 2020
day = 2

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""
text1 = aocd.get_data(day=day, year=year)

def valid(line, pone=True):
    rule, password = line.split(': ')
    rng, char = rule.split()
    lo, hi = (int(x) for x in rng.split('-'))
    if pone:
        return lo <= password.count(char) <= hi
    return (password[lo-1] == char) ^ (password[hi-1] == char)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone = sum(valid(line) for line in text)

    ptwo = sum(valid(line, pone=False) for line in text)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
