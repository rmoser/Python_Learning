# Advent of Code
year = 2021
day = 11

import numpy as np
import aocd

text0 = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
text1 = aocd.get_data(day=day, year=year)

kernel = np.array([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

if __name__ == '__main__':
    text = text1
    arr = np.array([list(t) for t in text.strip().splitlines()]).astype(int)

    # arr = np.array([[int(c) for c in line] for line in text])

    r_max, c_max = arr.shape
    n = r_max * c_max
    print(0)
    print(arr)

    flashes = 0
    full_flashes = 0
    j = 0
    while j < 101 or not full_flashes:
        j += 1
        _flashes = 0

        arr += 1
        while (arr > 9).any():
            for i in np.ndindex(arr.shape):
                if arr[i] > 9:
                    _flashes += 1
                    arr[i] = -1
                    items = [tuple(x) for x in (i + kernel) if all([0 <= x[0] < r_max, 0 <= x[1] < c_max])]
                    for p in items:
                        if arr[p] >= 0:
                            arr[p] += 1
        arr[arr==-1] = 0
        if j <= 100:
            flashes += _flashes

        if (arr == 0).all():
            print(f"Full flash: {j} {arr}")
            full_flashes = j

        print(j)
        print(arr)

    print(f"AOC {year} day {day}  Part One: {flashes}")

    print(f"AOC {year} day {day}  Part Two: {full_flashes}")
