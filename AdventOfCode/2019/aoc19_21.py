# Advent of Code
year = 2019
day = 22

import numpy as np
import aocd
from functools import cache
from icecream import ic

text0 = """
deal with increment 7
deal into new stack
deal into new stack
"""

text0 = """
cut 6
deal with increment 7
deal into new stack
"""

text0 = """
deal with increment 7
deal with increment 9
cut -2
"""

text0 = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""

text1 = aocd.get_data(day=day, year=year)

@cache
def deal_with_increment(n, l):
    arr = np.zeros(l, dtype=int)
    for i in range(l):
        _idx = (i * n) % l
        arr[_idx] = i
    return arr.tolist()

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    if text == text0:
        arr = np.array(range(10), dtype=int)
    else:
        arr = np.array(range(10007), dtype=int)

    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    for line in text:
        if line == 'deal into new stack':
            arr = arr[::-1]
            continue

        if line.startswith('deal with increment '):
            n = int(line.split(' ')[-1])
            arr = arr[deal_with_increment(n, len(arr))]
            continue

        if line.startswith('cut '):
            n = int(line.split(' ')[-1])
            arr = np.roll(arr, -(n % len(arr)))

    ic(arr)
    if len(arr) == 10:
        raise()

    pone = np.where(arr == 2019)[0][0]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
