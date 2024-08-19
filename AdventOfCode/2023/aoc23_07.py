# Advent of Code
year = 2023
day = 7

import numpy as np
import aocd
from functools import cmp_to_key

text0 = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
text1 = aocd.get_data(day=day, year=year)

cards = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    '1': 1
}


def score(hand, pone=True):
    d = dict()
    for c in hand:
        d[c] = d.get(c, 0) + 1

    j = 0
    if not pone:
        j = d.pop('J', 0)

    vals = sorted(d.values())

    if not vals:
        # All wilds
        return 5

    vals[-1] = vals[-1] + j

    if vals[-2:] == [2, 3]:
        return 3.2

    if vals[-2:] == [2, 2]:
        return 2.2

    return vals[-1]


def gt(a, b, pone=True):
    _a = score(a, pone)
    _b = score(b, pone)

    if _a != _b:
        return _a > _b

    for _a, _b in zip(a, b):
        if _a != _b:
            if not pone and 'J' in (_a, _b):
                return _b == 'J'
            return cards[_a] > cards[_b]

    return False


def lt(a, b, pone=True):
    return gt(b, a, pone)


def cmp(a, b):
    if lt(a, b):
        return -1
    if gt(a, b):
        return 1
    return 0


def cmp2(a, b):
    if lt(a, b, pone=False):
        return -1
    if gt(a, b, pone=False):
        return 1
    return 0


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    hands = {}
    for line in text:
        line = line.split()
        hands[line[0]] = int(line[1])

    result = sorted(list(hands.keys()), key=cmp_to_key(cmp))

    pone = 0
    for i, h in enumerate(result):
        pone += (i+1) * hands[h]

    ptwo = 0
    result = sorted(list(hands.keys()), key=cmp_to_key(cmp2))
    for i, h in enumerate(result):
        ptwo += (i+1) * hands[h]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
