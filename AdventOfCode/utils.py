#  Utility Functions to reuse

import numpy as np
import aocd
import math
import itertools
import scipy as sp
from scipy import ndimage


def text_format(text, foreground=None, background=None, style=None):
    colors = {
        None: 0,

        # Font Styles
        'normal': 0,
        'bold': 1,
        'light': 2,
        'italic': 3,
        'underline': 4,
        'blink': 5,

        # Foreground colors
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'purple': 35,
        'cyan': 36,
        'white': 37,

        # Background colors
        'b_black': 40,
        'b_red': 41,
        'b_green': 42,
        'b_yellow': 43,
        'b_blue': 44,
        'b_purple': 45,
        'b_cyan': 46,
        'b_white': 47,
    }

    def fmt(text, codes=[0]):
        if not isinstance(codes, list):
            codes = [codes]
        codes = ';'.join([str(x) for x in codes])
        return f"\033[{codes}m" + text + "\033[0;0;0m"

    if foreground is None and background is None:
        col = 12
        s = fmt(f'\nCODE{" "*(col-4)}RESULT\n', [0])
        for k, v in colors.items():
            if k:
                s += f'{k}:{" "*(col-len(k)-1)}{fmt((text if text else k), v)}\n'

        print(s)
        return

    if background and background in colors and not background.startswith('b_'):
        background = f'b_{background}'

    return fmt(text, sorted(set([colors[c] for c in (foreground, background, style) if c in colors])))


def show_string(screen, start=None, end=None, path=None, dist=None, translate=None):
    if translate is None:
        # zeros to centered dot (·), ones to hash (#).
        translate = {ord('1'): ord('#'), ord('0'): ord('·')}

    # Convert to str array
    arr = screen.astype(int).astype(str)

    # Translation from int values to characters
    if translate:
        arr = np.char.translate(arr, translate)

    # Extend width to support format codes
    dt = np.dtype(('U', arr.dtype.itemsize // arr.dtype.alignment + 30))
    arr = arr.astype(dt)
    print(dt)

    if start:
        arr[start] = text_format(arr[start], foreground='normal', background='green', style='bold')
    if end:
        arr[end] = text_format(arr[end], foreground='normal', background='red', style='bold')
    if path:
        # Highlight path, excluding start and end
        intermed = [tuple(p) for p in set(path) - set(start) - set(end)]
        # print(intermed)
        for p in intermed:
            arr[p] = text_format(arr[p], foreground='black', background='white', style='bold')
            # print(p, ": ", len(arr[p]))


    if dist:
        pad = max(len(str(k)) for k in dist)

    w = len(str(arr.shape[0]))
    result = f"{' ' * w} {''.join(str(s % 10) for s in range(screen.shape[1]))}"
    for r in range(arr.shape[0]):
        # print(f"{r}", ''.join(screen[r].astype(str)).replace('0', '\u25AF').replace('1', '\u25AE'))
        result += f"\n{str(r).rjust(w)} {''.join(arr[r])}"

    return result


def show(screen, start=None, end=None, path=None, dist=None):
    result = show_string(screen, start=start, end=end, path=path, dist=dist)
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
    print("text_format(string):")
    print('abc' + text_format('def', 'black', 'white', 'italic') + 'ghi')
    print()

    print("show(maze):")
    maze = np.zeros(shape=(10, 10), dtype=int)
    start = (0, 0)
    end = (9, 9)
    path = [(0,0)]
    for i in range(1, 10):
        path.append((i-1, i))
        path.append((i, i))

    show(maze, start, end, path)

