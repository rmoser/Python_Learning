# Advent of Code
year = 2016
day = 3

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = np.array([line.split() for line in text], dtype=int)

    a = arr.copy()
    a.sort(axis=1)

    pone = (a[:, :2].sum(axis=1) > a[:, 2]).sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    # b = np.array([arr[i:i+3, :].T for i in range(0, arr.shape[0], 3)]).reshape(arr.shape)
    b = np.array([arr[:, 0], arr[:, 1], arr[:, 2]]).reshape(arr.shape)
    b.sort(axis=1)
    ptwo = (b[:, :2].sum(axis=1) > b[:, 2]).sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
