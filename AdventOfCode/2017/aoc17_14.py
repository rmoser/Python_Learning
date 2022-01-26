# Advent of Code
year = 2017
day = 14

import numpy as np
import aocd
import utils
from scipy.ndimage.measurements import label


text0 = """flqrgnkx"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    arr = np.zeros((128, 128), dtype=int)
    for i in range(128):
        inst = f"{text}-{i}"
        b = utils.knot(inst)
        arr[i] = [int(c) for c in bin(int(b, 16))[2:].rjust(128, '0')]

    pone = arr.sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = label(arr)[1]
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
