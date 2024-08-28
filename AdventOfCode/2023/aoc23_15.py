# Advent of Code
from collections import OrderedDict

year = 2023
day = 15

import numpy as np
import aocd
import os
import functools
from collections import OrderedDict
from pprint import pprint
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"

text0 = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
text1 = aocd.get_data(day=day, year=year)

@functools.cache
def hash(word):
    score = 0
    for c in word:
        score += ord(c)
        score *= 17
        score %= 256
    return score


if __name__ == '__main__':
    text = text1
    text = text.strip().splitlines()[0].split(',')

    pone = sum(hash(w) for w in text)
    print(f"AOC {year} day {day}  Part One: {pone}")

    arr = [OrderedDict() for _ in range(256)]

    for w in text:
        if w.endswith('-'):
            label = w[:-1]
            box = hash(label)
            d = arr[box]
            if label in d:
                d.pop(label)
        else:
            label, num = w.split('=')
            num = int(num)
            box = hash(label)
            arr[box][label] = num

    ptwo = 0
    for box in range(len(arr)):
        if not arr[box]:
            continue
        for i, (k, v) in enumerate(arr[box].items()):
            ptwo += (box+1) * (i+1) * v

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
