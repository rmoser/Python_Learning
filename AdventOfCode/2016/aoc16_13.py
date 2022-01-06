# Advent of Code
year = 2016
day = 13

import numpy as np
import aocd
import math
import itertools
import scipy as sp
from scipy import ndimage

from utils import show, valid_path

text0 = "10"
text1 = aocd.get_data(day=day, year=year)


def calc(x, y, i):
    s = x*x + 3*x + 2*x*y + y + y*y + i

    # a = sum([(s >> i) & 1 for i in range(1+math.ceil(math.log2(s)))])
    return bin(s).count('1') & 1


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    if text == text0:
        maze_dim = 10
        start = (1, 1)
        end = (4, 7)
        # end = (5, 7)
    else:
        maze_dim = 100
        start = (1, 1)
        end = (39, 31)

    value = int(text.strip())

    maze = np.zeros((maze_dim, maze_dim), dtype=int)
    for y, x in np.ndindex(maze.shape):
        maze[y, x] = calc(x, y, value)

    # show(maze, start, end)

    path = valid_path(maze, start, end)

    show(maze, start, end, path)

    pone = len(path)-1  # Subtract starting position

    paths, points = valid_path(maze, start, end, iters=50)

    ptwo = len(points)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
