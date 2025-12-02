# Advent of Code
import math

year = 2025
day = 2

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic


text0 = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""
text1 = aocd.get_data(day=day, year=year)

def split(lo: int, hi: int) -> list[tuple[int, int]]:
    len_lo = len(str(lo))
    len_hi = len(str(hi))

    if len_lo == len_hi:
        return [(lo, hi)]

    result = []
    for l in range(len_lo, len_hi+1):
        if l == len_lo:
            _min = lo
        else:
            _min = 10 ** (l-1)
        if l == len_hi:
            _max = hi
        else:
            _max = 10 ** l - 1
        result.append((_min, _max))

    # ic(result)
    return result

def score(lo, hi):
    result = set(), set()

    len_lo = len(str(lo))
    len_hi = len(str(hi))

    if len_lo != len_hi:
        raise ValueError(f"Invalid range: ({lo}, {hi})")

    for substr_len in range(1, len_lo // 2 + 1):
        repeats, remainder = divmod(len_lo, substr_len)

        if remainder != 0:
            continue

        for i in range(int(str(lo)[:substr_len]), int(str(hi)[:substr_len]) + 1):
            x = int(str(i) * repeats)
            if lo <= x <= hi:
                result[1].add(x)
                if repeats == 2:
                    result[0].add(x)

    return result


def invalid(lo, hi):
    # print("invalid(", min, ",", max, ")")
    result = set(), set()

    split_ranges = split(lo, hi)
    for lo, hi in split_ranges:
        if not lo or not hi:
            ic("Skip empty range:", lo, hi)
            continue

        ic(lo, hi)
        r = score(lo, hi)
        result[0].update(r[0])
        result[1].update(r[1])

    return result

ic.disable()

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    vals = set(), set()
    text = text[0].split(',')
    for word in text:
        if not word:
            continue
        start, end = (int(val) for val in word.split('-'))
        ic(start, end)
        r = invalid(start, end)
        ic(start, end, r)
        vals[0].update(r[0])
        vals[1].update(r[1])

    pone = sum(vals[0])
    ptwo = sum(vals[1])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
