# Advent of Code
year = 2023
day = 0

import numpy as np
import aocd

text0 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    arr = np.array([[c for c in line] for line in text])
    symbols = np.bitwise_not(np.isin(arr, list('0123456789.')))
    _s = np.where(symbols)
    s = np.array(list(zip(*_s)))
    _a = np.where(np.char.isdigit(arr))
    a = np.array(list(zip(*_a)))

    d = lambda x: np.abs(x-s).max(axis=1).min()


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
