# Advent of Code
year = 2016
day = 13

import numpy as np
import aocd
import math
import itertools

text0 = "10"
text1 = aocd.get_data(day=day, year=year)


def calc(x, y, i):
    s = x*x + 3*x + 2*x*y + y + y*y + i

    a = sum([(s >> i) & 1 for i in range(math.ceil(math.log2(s)))])

    return a & 1


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


def show(screen, start=None, end=None, path=None):
    arr = np.char.translate(screen.astype(int).astype(str), {ord('1'): ord('#'), ord('0'): ord('\u00B7')})

    if start is not None:
        arr[start] = bold(arr[start], 'green')
    if end is not None:
        arr[end] = bold(arr[end], 'red')
    if path is not None:
        for p in path[:-1]:
            arr[tuple(p)] = ' '

    w = len(str(arr.shape[0]))
    result = f"{' ' * w} {''.join(str(s % 10) for s in range(screen.shape[1]))}"
    for r in range(arr.shape[0]):
        # print(f"{r}", ''.join(screen[r].astype(str)).replace('0', '\u25AF').replace('1', '\u25AE'))
        result += f"\n{str(r).rjust(w)} {''.join(arr[r])}"

    print(result)


def valid_path(maze, start, end):
    moves = np.array([(1, 0), (-1, 0), (0, 1), (-1, 0)])
    paths = [[start]]
    max_moves = np.prod(maze.shape)
    while True:
        path = paths.pop()
        if len(path) >= max_moves:
            return []

        pos = path[-1]
        for move in moves:
            new_pos = tuple(pos + move)
            if new_pos == end:
                return path + [new_pos]
            if new_pos in path:
                continue
            if (min(new_pos) < 0) or (new_pos >= np.array(maze.shape)).any():
                continue
            if maze[new_pos] == 0:
                paths.append(path + [new_pos])


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    if text == text0:
        maze_dim = 10
        start = (1, 1)
        end = (7, 4)
        end = (5, 7)
    else:
        maze_dim = 100
        start = (1, 1)
        end = (31, 39)

    value = int(text.strip())

    maze = np.zeros((maze_dim, maze_dim), dtype=int)
    for y, x in np.ndindex(maze.shape):
        maze[y, x] = calc(x, y, value)

    # show(maze, start, end)

    path = valid_path(maze, start, end)

    show(maze, start, end, path)

    pone = len(path)-1  # Subtract starting position

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
