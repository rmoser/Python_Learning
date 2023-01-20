# Advent of Code
year = 2022
day = 1

import numpy as np
import aocd

text0 = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
text1 = aocd.get_data(day=day, year=year)


def parse(text):
    inv = [x.split('\n') for x in text.strip().split('\n\n')]
    return [[int(y) for y in x] for x in inv]


def get_elfs(inv):
    return np.array([np.sum(x) for x in inv])


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    elfs = get_elfs(parse(text1))

    pone = elfs.max()

    print(f"AOC {year} day {day}  Part One: {pone}")

    elfs.sort()
    ptwo = elfs[-3:].sum()

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
