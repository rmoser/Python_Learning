# Advent of Code
year = 2015
day = 18

import numpy as np
import aocd

text0 = """ 
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""
text1 = aocd.get_data(day=day, year=year)


def calc(arr, part=1):
    shape = np.array(list(arr.shape)) + 2

    new_arr = np.zeros(shape, dtype=np.uint8)
    new_arr[1:-1, 1:-1] = arr

    counts = new_arr[2:, 2:] + new_arr[2:, 1:-1] + new_arr[2:, :-2]
    counts += new_arr[1:-1, 2:] + new_arr[1:-1, :-2]
    counts += new_arr[:-2, 2:] + new_arr[:-2, 1:-1] + new_arr[:-2, :-2]

    result = arr * np.bitwise_and(counts >= 2, counts <= 3) + (1-arr) * (counts == 3)
    if part == 2:
        result[(0, 0, -1, -1), (0, -1, -1, 0)] = 1

    return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = (np.array([list(line) for line in text]) == '#').astype(np.uint8)

    for _ in range(100):
        arr = calc(arr)

    pone = arr.sum()

    arr = (np.array([list(line) for line in text]) == '#').astype(np.uint8)

    for _ in range(100):
        arr = calc(arr, part=2)

    ptwo = arr.sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
