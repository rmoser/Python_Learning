# Advent of Code
year = 2020
day = 3

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import math

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""
text1 = aocd.get_data(day=day, year=year)

def count_trees(array, step):
    pos = (0, 0)
    count = array[pos]
    while pos[0] < array.shape[0]-1:
        pos += np.array(step)
        pos[1] = pos[1] % array.shape[1]
        pos = tuple(pos.tolist())
        count += array[pos]
    return count

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    array = np.array(np.array([list(line) for line in text]) == '#').astype(int)
    print(array)

    pone = count_trees(array, (1, 3))

    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]

    ptwo = math.prod(count_trees(array, slope) for slope in slopes)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
