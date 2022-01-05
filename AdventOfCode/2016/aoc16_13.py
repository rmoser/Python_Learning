# Advent of Code
year = 2016
day = 13

import numpy as np
import aocd
import math
import itertools
import scipy as sp
from scipy import ndimage

text0 = "10"
text1 = aocd.get_data(day=day, year=year)


def calc(x, y, i):
    s = x*x + 3*x + 2*x*y + y + y*y + i

    # a = sum([(s >> i) & 1 for i in range(1+math.ceil(math.log2(s)))])
    return bin(s).count('1') & 1


def bold(text, color=None):
    colors = {
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'darkcyan': '\033[36m',
        'blue': '\033[94m',
        'green': '\033[42m',
        'yellow': '\033[93m',
        'red': '\033[41m',
        'bold': '\033[1m',
        'underline': '\033[4m'
    }
    end = '\033[0m'

    if color is None:
        color = 'bold'

    c = [colors[c] for c in np.atleast_1d(color) if c in colors]
    if len(c) == 0:
        return text

    return ''.join(c) + text + (end * len(c))


def repr(screen, start=None, end=None, path=None, dist=None):
    arr = np.char.translate(screen.astype(int).astype(str), {ord('1'): ord('#'), ord('0'): ord('\u00B7')})

    if start:
        arr[start] = bold(arr[start], 'green')
    if end:
        arr[end] = bold(arr[end], 'red')
    if path:
        for p in path[:-1]:
            arr[tuple(p)] = ' '

    if dist:
        pad = max(len(str(k)) for k in dist)

    w = len(str(arr.shape[0]))
    result = f"{' ' * w} {''.join(str(s % 10) for s in range(screen.shape[1]))}"
    for r in range(arr.shape[0]):
        # print(f"{r}", ''.join(screen[r].astype(str)).replace('0', '\u25AF').replace('1', '\u25AE'))
        result += f"\n{str(r).rjust(w)} {''.join(arr[r])}"

    return result


def show(screen, start=None, end=None, path=None, dist=None):
    result = repr(screen, start=start, end=end, path=path, dist=dist)
    print(result)


def valid_path(maze, start, end, paths=None, iters=-1, debug=False):
    moves = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
    if not paths:
        paths = [[start]]
    elif not isinstance(paths[0], list):
        paths = [paths]

    pos_dist = {start: 0}

    max_moves = np.prod(maze.shape)
    while True:
        for _ in range(len(paths)):
            path = paths.pop(0)
            if len(path) >= max_moves:
                return []

            pos = path[-1]
            for move in moves:
                new_pos = pos + move
                new_pos_tuple = tuple(new_pos)
                if (new_pos == end).all():
                    pos_dist[new_pos_tuple] = len(path)  # len(path) includes the start point already, so no need to increment for the end point
                    return path + [new_pos_tuple]
                if new_pos_tuple in pos_dist:  # Shorter path to this point already exists
                    continue
                if (new_pos < 0).any() or (new_pos >= maze.shape).any():
                    continue
                if maze[new_pos_tuple] == 0:
                    paths.append(path + [new_pos_tuple])
                    pos_dist[new_pos_tuple] = len(path)  # len(path) includes the start point already, so no need to increment for the end point
                if debug:
                    print(move, path)

            if debug:
                print('\n Paths: ', paths)

        iters -= 1
        if iters == 0:
            return paths, pos_dist


def areas(maze):
    return ndimage.label(maze < 1)


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
