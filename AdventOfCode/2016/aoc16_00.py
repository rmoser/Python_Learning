# Advent of Code
year = 2016
day = 0

import numpy as np
import aocd

text0 = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""
text1 = aocd.get_data(day=day, year=year)

discs = dict()

# Dirty Enums
POS = 0
START = 1
PERIOD = 2

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()
    for line in text:
        line = line.split()
        n = int(line[1][1:])
        period = int(line[3])
        start = int(line[-1][:-1])
        discs[n] = [start, n, start, period]


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
