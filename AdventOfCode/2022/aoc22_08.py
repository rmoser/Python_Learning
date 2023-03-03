# Advent of Code
year = 2022
day = 8

import numpy as np
import aocd

text0 = """
30373
25512
65332
33549
35390
"""
text1 = aocd.get_data(day=day, year=year)


def visible_count(arr):
    if len(arr) <= 1:
        return 0

    n = 0
    h = arr[0]
    for t in arr[1:]:
        n += 1
        if t >= h:
            return n

    return n


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().replace('\n', ';')
    text = " ".join(list(text))

    grid = np.asarray(np.mat(text))
    visible = np.zeros(grid.shape, dtype=bool)

    # Edges visible
    visible[0] = True
    visible[:, 0] = True
    visible[grid.shape[0]-1] = True
    visible[:, grid.shape[1]-1] = True

    # Iterate on interior coordinates
    for r in range(1, grid.shape[0]-1):
        for c in range(1, grid.shape[1]-1):

            # Row-wise visible
            if (grid[r, c] > grid[r, 0:c]).all():
                visible[r, c] = True
                continue
            if (grid[r, c] > grid[r, c+1:]).all():
                visible[r, c] = True
                continue

            # Column-wise visible
            if (grid[r, c] > grid[0:r, c]).all():
                visible[r, c] = True
                continue
            if (grid[r, c] > grid[r+1:, c]).all():
                visible[r, c] = True
                continue

    pone = visible.sum()

    look_west = np.zeros(shape=grid.shape, dtype=int)
    look_east = look_west.copy()
    look_north = look_west.copy()
    look_south = look_west.copy()

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            _r = grid.shape[0] - r - 1
            _c = grid.shape[1] - c - 1

            if c > 0:
                look_west[r, c] = visible_count(np.flip(grid[r, :c+1]))
                look_east[r, c] = visible_count(grid[r, c:])

            if r > 0:
                look_north[r, c] = visible_count(np.flip(grid[:r+1, c]))
                look_south[r, c] = visible_count(grid[r:, c])

    dist = look_north * look_south * look_west * look_east
    ptwo = dist.max()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
