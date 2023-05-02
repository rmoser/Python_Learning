# Advent of Code
year = 2018
day = 6

import numpy as np
import aocd

text0 = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    coords = list()
    for coord in text:
        x, y = [int(x) for x in coord.split(', ')]
        coords.append(np.array((x, y)))

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
