# Advent of Code
year = 2019
day = 22

import numpy as np
import aocd
from functools import cache
from icecream import ic
import utils


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
global text

@cache
def deal_with_increment(n, l):
    _arr = np.zeros(l, dtype=int)
    for i in range(l):
        _idx = (i * n) % l
        _arr[_idx] = i
    return _arr.tolist()

@cache
def run(n, value):
    idx = value
    # arr = np.array(range(n), dtype=int)

    for line in text.splitlines():
        if line == 'deal into new stack':
            idx = n - idx -1
            # arr = arr[::-1]
            continue

        if line.startswith('deal with increment '):
            increment = int(line.split(' ')[-1])
            idx = (idx * increment) % n
            # arr = arr[deal_with_increment(n, len(arr))]
            continue

        if line.startswith('cut '):
            increment = int(line.split(' ')[-1])
            idx = (idx - increment) % n
            # arr = np.roll(arr, -(n % len(arr)))

        # ic(n, idx)
    return idx

def run2(n, value, cycles):
    b = run(n, 0)
    m = run(n, 1) % n

    return ((b * cycles) % n + ((m * value % n) * cycles) % n) % n

def run0(n):
    arr = np.array(range(n), dtype=int)

    for line in text.splitlines():
        if line == 'deal into new stack':
            arr = arr[::-1]
            continue

        if line.startswith('deal with increment '):
            increment = int(line.split(' ')[-1])
            # idx = (idx * increment) % n
            arr = arr[deal_with_increment(increment, len(arr))]
            continue

        if line.startswith('cut '):
            increment = int(line.split(' ')[-1])
            # idx = (idx - increment) % n
            arr = np.roll(arr, -(increment % len(arr)))

        # ic(n, idx)
    return arr

def _test_run(n, text):
    arr = np.zeros(n, dtype=int)
    for i in range(n):
        arr[run(n, text, i)] = i
        ic(arr)
    return arr

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    if text == text1:
        n = 10007, 119315717514047
    else:
        n = 10, 10

    pone = run2(n[0], 2019, 1)
    print(f"AOC {year} day {day}  Part One: {pone}")

    # idx0 = run(n[1], 2020)

    # iters = 1
    # idx = idx0
    # while True:
    #     idx = run(n[1], idx)
    #     iters += 1
    #     ic(iters, idx)
    #     if idx == 2020:
    #         break
    #
    # ic(iters)

    # idx = 2020
    # for i in range(101741582076661):
    #     idx = run(n[1], idx)
    #     print('\r', i, idx, end='\t\t\t\t\t\t')
    #
    # ptwo = idx

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
