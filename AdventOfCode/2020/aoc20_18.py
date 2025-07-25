# Advent of Code
year = 2020
day = 18

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import math

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """1 + 2 * 3 + 4 * 5 + 6"""
text0 = "1 + (2 * 3) + (4 * (5 + 6))"
text1 = aocd.get_data(day=day, year=year)

def calc(text, ptwo=False):
    # print(f'calc: "{text}"')
    if not text:
        return ''
    text = text.split()
    if not ptwo:
        a = int(text[0])
        for op, b in zip(text[1::2], text[2::2]):
            b = int(b)
            match op:
                case '+':
                    a += b
                case '*':
                    a *= b
        return str(a)

    while '+' in text:
        i = text.index('+')
        a = int(text[i-1])
        b = int(text[i+1])
        text[i-1] = str(a + b)
        text.pop(i)  # Remove +
        text.pop(i)  # Remove b

    text = str(math.prod([int(x) for x in text if x != '*']))

    return text


def parse(text, ptwo=False):
    while '(' in text:
        i = len(text) - text[::-1].index('(') - 1
        j = i + 1 + text[i:].index(')')
        text = text[:i] + calc(text[i+1:j-1], ptwo) + text[j:]
        # print(text)
    return calc(text, ptwo)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone = sum(int(parse(t)) for t in text)
    ptwo = sum(int(parse(t, ptwo=True)) for t in text)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
