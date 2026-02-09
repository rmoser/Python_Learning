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
global text, instructions
m = None
b = None


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

def run3(n, value):
    values = [value]
    values_set = set()
    idx = value
    i = 0
    while True:
        i += 1
        idx = run(n, idx)
        values.append(idx)
        if idx in values_set:
            return values
        values_set.add(idx)
        if i == 1000000:
            return values



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

def steps(n):
    arr = np.zeros((n, len(instructions)+1), dtype=int)
    arr[:, 0] = np.arange(n)

    for row in range(n):
        for i, line in enumerate(instructions):
            if line == 'deal into new stack':
                arr[:, i+1] = arr[::-1, i]
                continue

            if line.startswith('deal with increment '):
                increment = int(line.split(' ')[-1])
                # idx = (idx * increment) % n
                arr[:, i+1] = arr[deal_with_increment(increment, len(arr)), i]
                continue

            if line.startswith('cut '):
                increment = int(line.split(' ')[-1])
                # idx = (idx - increment) % n
                arr[:, i+1] = np.roll(arr[:, i], -(increment % len(arr)))
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

    text = text1
    if text == text1:
        _n = 10007, 119315717514047
    else:
        _n = 10, 10
    instructions = text.strip().splitlines()

    pone = run(_n[0], 2019)
    print(f"AOC {year} day {day}  Part One: {pone}")

    n = _n[1]
    id0 = 2020
    id1 = run(n, id0)
    b = id0
    m = (id1-id0) % n

    def p(i, t, n):
        return (b*(m+1)**int(t-1)%n + (i*m**t)%n) % n

    # def p(i, t, n):
    #     return (b + i*m) % n

    data = np.zeros(10, dtype=int)
    data[0] = 2019
    for i in range(1, 10):
        data[i] = run(_n[0], data[i-1])

    xarr = run3(_n[1], 2020)


    # ptwo = p(2020, 101741582076661, n[1])

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
