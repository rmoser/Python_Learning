# Advent of Code
year = 2017
day = 2

import numpy as np
import aocd
import itertools

text0 = """
5 1 9 5
7 5 3
2 4 6 8
"""

textA = """
5 9 2 8
9 4 7 3
3 8 6 5
"""

text1 = aocd.get_data(day=day, year=year)


def get_stat(arr):
    for a, b in itertools.combinations(sorted(arr, reverse=True), r=2):
        if a % b == 0:
            return a // b


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    data = [np.array(x.split()).astype(int) for x in text]

    pone = sum(a.ptp() for a in data)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = sum(get_stat(a) for a in data)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
