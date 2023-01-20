# Advent of Code
year = 2016
day = 20

import numpy as np
import aocd

text0 = """
5-8
0-2
4-7
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    ip = np.ones(shape=2**32, dtype=bool)

    for line in text:
        a, b = [int(x) for x in line.split('-')]
        ip[a:b+1] = False

    pone = ip.argmax()
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = ip.sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
