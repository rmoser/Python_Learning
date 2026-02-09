# Advent of Code
import utils

year = 2019
day = 24

import numpy as np
import scipy as sp
import aocd
import itertools as it
from icecream import ic

text0 = """
....#
#..#.
#..##
..#..
#....
"""
#
# text0 = """
# .....
# .....
# .....
# #....
# .#...
# """

text1 = aocd.get_data(day=day, year=year)

class Grid:
    def __init__(self, arr):
        self.arr = arr.copy()

    def biodiversity(self):
        return (2 ** np.nonzero(self.arr.flatten())[0]).sum()

    def run(self, recurse=False):
        neighbors = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=int)
        memory = {self.biodiversity()}

        _arr = self.arr.copy()

        if not recurse:
            while True:
                n = sp.signal.convolve2d(self.arr, neighbors, mode='same')
                _arr[np.bitwise_and(self.arr == 1, n != 1)] = 0
                _arr[np.bitwise_and(self.arr == 0, np.bitwise_or(n == 1, n == 2))] = 1
                self.arr[:,:] = _arr
                b = self.biodiversity()
                if b in memory:
                    return b
                memory.add(b)

        return None


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    arr = Grid((utils.map_from_text(text) == '#').astype(int))

    pone = arr.run()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
