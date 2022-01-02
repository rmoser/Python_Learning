# Advent of Code
year = 2015
day = 25

import numpy as np
import aocd

text0 = """ 
"""
text1 = aocd.get_data(day=day, year=year)


def op(x):
    return x * 252533 % 33554393


def sum_1_n(n):
    return n * (n + 1) // 2


def fact(n):
    d = {}
    v = n
    for i in range(2, int(n**0.5) + 1):
        d[i] = 0
        while v % i == 0:
            d[i] += 1
            v = v // i
    if v > 1:
        d[v] = 1

    return {k: v for k, v in d.items() if v}


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split()

    row = int(text[-3].replace(',', ''))
    col = int(text[-1].replace('.', ''))

    c = row + col + 1
    r = row + 1

    arr = np.zeros(shape=(r, c), dtype=np.int64)

    arr[1] = [sum_1_n(n) for n in range(c)]

    # r = 1
    # r += 1
    # arr[r, 1:1-r] = -1 + arr[r-1, 2:c+2-r]
    # arr

    for r in range(2, arr.shape[0]):
        arr[r, 1:1 - r] = -1 + arr[r - 1, 2:c + 2 - r]

    n = arr[row, col]-1

    x = 20151125
    for _ in range(n):
        x = op(x)

    pone = x

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
