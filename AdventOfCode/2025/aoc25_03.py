# Advent of Code
year = 2025
day = 3

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic

text0 = """
987654321111111
811111111111119
234234234234278
818181911112111
"""
text1 = aocd.get_data(day=day, year=year)

def mult(items):
    return int(''.join(str(c) for c in items))

def get_index(items) -> int:
    for i in range(len(items)-1):
        if items[i+1] > items[i]:
            return i
    return -1  # Items are in descending order

def max_joltage(bank):
    ic('\n\n\n', bank)
    results = [[0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    if not np.iterable(bank):
        bank = str(bank)

    for c in bank:
        if isinstance(c, str):
            c = int(c)

        for result in results:
            i = get_index(result)
            min_result = min(result)
            ic(c, i, min_result, result)
            if i > -1:
                ic("Pop")
                result.pop(i)
                result.append(c)
            elif c > min_result:
                ic("Remove")
                result.remove(min_result)
                result.append(c)
            else:
                ic("NOP")
            ic(result)

    return [mult(r) for r in results]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    ic.disable()

    pone, ptwo = 0, 0

    for line in text:
        val = max_joltage(line)
        ic(line, val)
        pone += val[0]
        ptwo += val[1]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
