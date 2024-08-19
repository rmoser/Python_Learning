# Advent of Code
year = 2023
day = 3

import numpy as np
import scipy as sp
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

    arr = np.array([list(x) for x in text])
    symbols = np.where(np.bitwise_not(np.isin(arr, list('0123456789.'))))  # Symbol positions
    nums = np.where(np.chararray.isnumeric(arr))
    nums_c = np.matrix(nums).T
    arr[nums_c[0]]
    d_x = np.abs(nums[0] - symbols[0][:,None]) <= 1
    d_y = np.abs(nums[1] - symbols[1][:,None]) <= 1
    d_xy = np.bitwise_and(d_x, d_y).any(axis=0)
    n = 0
    s1, s2 = 0, 0
    for x, y in zip(*nums):



    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
