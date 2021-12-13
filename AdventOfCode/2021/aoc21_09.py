# Advent of Code
year = 2021
day = 9

import numpy as np
import aocd
import scipy as sp
from scipy import ndimage


text0 = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    text = text1
    text = np.array([list(t) for t in text.strip().splitlines()]).astype(int)

    kernel = np.array([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
    kernel2 = np.array([(-1, 0), (0, -1), (0, 1), (1, 0)])

    risk = 0
    r_max, c_max = text.shape
    for r, c in np.ndindex(text.shape):
        items = [tuple(x) for x in ((r, c) + kernel) if all([0 <= x[0] < r_max, 0 <= x[1] < c_max])]
        low = np.min([text[i] for i in items])
        if text[(r, c)] < low:
            risk += 1 + text[(r, c)]

    basins = ndimage.label(text < 9)
    n = basins[1]
    counts = [(basins[0] == i+1).sum() for i in range(n)]

    top_three = [counts[x] for x in np.argsort(counts)[-3:]]

    print(f"AOC {year} day {day}  Part One: {risk}")

    print(f"AOC {year} day {day}  Part Two: {np.product(top_three)}")
