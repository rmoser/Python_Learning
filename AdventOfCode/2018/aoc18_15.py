# Advent of Code
year = 2018
day = 15

import numpy as np
import aocd

text0 = """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
"""
text1 = aocd.get_data(day=day, year=year)


def show(arr):
    for line in arr:
        print('\0' + ''.join(line))
    

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.strip('\n').splitlines()
    arr = np.array([list(x) for x in text])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
