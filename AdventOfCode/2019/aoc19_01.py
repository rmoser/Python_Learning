# Advent of Code
year = 2019
day = 1

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)


def fuel(x):
    y = 0
    while x >= 9:
        x = x // 3 - 2
        y += x
    return y


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    pone = sum([int(x) // 3 - 2 for x in text])
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = sum([fuel(int(x)) for x in text])
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
