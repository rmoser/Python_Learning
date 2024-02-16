# Advent of Code
year = 2018
day = 0

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
