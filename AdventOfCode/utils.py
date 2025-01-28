#  Utility Functions to reuse
from __future__ import annotations

import numpy as np
import aocd
import math
import itertools
import scipy as sp
from functools import lru_cache
from scipy import ndimage
from scipy.stats import false_discovery_control
import pprint
import os

# Set authentication cookie
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

DEFAULT_TRANSLATE = {ord('1'): '#', ord('0'): '·'}

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
        return f"\033[{codes}m" + text + "\033[0m"

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
        translate = DEFAULT_TRANSLATE

    # Convert to str array
    if np.issubdtype(screen.dtype, np.integer):
        arr = screen.astype(int).astype(str)

        # Translation from int values to characters
        if translate:
            arr = np.char.translate(arr, translate)

    else:
        arr = screen.copy()

    if not start:
        start = set()
    elif isinstance(start[0], tuple):
        start = set([tuple(p) for p in start])
    else:
        start = {tuple(start)}

    if not end:
        end = set()
    elif isinstance(end[0], tuple):
        end = set([tuple(p) for p in end])
    else:
        end = {tuple(end)}

    path = set([tuple(p) for p in path]) - start - end if path else set()

    pos_max_length = max(len(x) for x in arr.flatten())
    if pos_max_length > 1:
        pos_max_length += 1  # Add space between cols if data has multiple chars

    for p in start | end | path:
        c = arr[p].rjust(pos_max_length)
        if p in start:
            _c = text_format(c, foreground='black', background='green', style='bold')
        elif p in end:
            _c = text_format(c, foreground='black', background='red', style='bold')
        else:
            _c = text_format(c, foreground='black', background='white', style='bold')

        # Update array data width when necessary to avoid overruns
        if len(_c) > arr.dtype.itemsize // arr.dtype.alignment:
            dt = np.dtype(('U', len(_c)))  # Guess at how much larger it needs to be
            arr = arr.astype(dt)
        arr[p] = _c

    if dist:
        pad = max(len(str(k)) for k in dist)

    w = len(str(arr.shape[0]))
    result = f"{' ' * w} {''.join(f'{str(s % 10 ** pos_max_length):>{pos_max_length}}' for s in range(arr.shape[1]))}"
    for r in range(arr.shape[0]):
        # print(f"{r}", ''.join(screen[r].astype(str)).replace('0', '\u25AF').replace('1', '\u25AE'))
        # result += f"\n{str(r).rjust(w)} {''.join(arr[r])}"
        result += f"\n{str(r).rjust(w)} {''.join(f'{c:>{pos_max_length}}' for c in arr[r])}"

    return result


def show(screen, start=None, end=None, path=None, dist=None, translate=None):
    if np.ndim(screen) <= 2:
        result = show_string(screen, start=start, end=end, path=path, dist=dist, translate=translate)
        print(result)
        return

    if screen.ndim == 3:
        for s in screen:
            print(show_string(s, start=start, end=end, path=path, dist=dist, translate=translate))
        return

    raise IndexError(f"Too many dimensions: {screen.ndim} > 3.")


def map_from_text(text):
    if isinstance(text, str):
        text = text.strip().split('\n')
    if isinstance(text, list):
        rows = len(text)
        cols = len(text[0])
        arr = np.full((rows, cols), fill_value='')
        for row, line in enumerate(text):
            arr[row] = list(line)
    return arr


def valid_path(maze, start, end, paths=None, iters=-1, debug=False):
    moves = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
    if not paths:
        paths = [[start]]
    elif not isinstance(paths[0], list):
        paths = [paths]

    pos_dist = {start: 0}

    max_moves = np.prod(maze.shape)

    result_paths = []

    while True:
        for _ in range(len(paths)):
            path = paths.pop(0)
            if len(path) >= max_moves:
                return []

            pos = path[-1]
            for move in moves:
                new_pos = pos + move  # type is np.array
                new_pos_tuple = tuple(new_pos)
                if (new_pos < 0).any() or (new_pos >= maze.shape).any():
                    continue
                if (new_pos == end).all():
                    pos_dist[new_pos_tuple] = len(path)  # len(path) includes the start point already, so no need to increment for the end point
                    return path + [new_pos_tuple], pos_dist
                if new_pos_tuple in pos_dist:  # Shorter path to this point already exists
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


def in_array(pos, arr):
    p = np.array(pos)
    return (p >= 0).all() and (p < arr.shape).all()


@lru_cache
def factor(n):
    d = {}
    if n == 0:
        return {0: 1}
    if n == 1:
        return {1: 1}
    if n < 4:
        d[n] = 1
        return d

    for i in np.arange(2, int(n**0.5)+1, dtype=np.int64):
        r = 0
        while r == 0:
            q, r = divmod(n, i)
            if r == 0:
                d[i] = d.get(i, np.int64(0)) + 1
                n //= i
    if n > 1:
        d[n] = 1
    return d


@lru_cache
def is_prime(n):
    if n < 2:
        return False
    return len(factor(n)) == 1


class BigInt():
    def __init__(self, value : (int, np.int32, np.int64, BigInt)):
        if isinstance(value, BigInt):
            self.value = value.value.copy()
        else:
            self.value = factor(value)
        self.__repr = np.int64(0)
        self.update()

    def clean(self):
        for k, v in self.value.items():
            if v == 0:
                self.value.pop(k)

    def update(self):
        self.clean()
        self.__repr = np.power(list(self.value.keys()), list(self.value.values())).prod()

    def __repr__(self) -> str:
        return str(self.__repr)

    def __str__(self) -> str:
        return pprint.pformat(self.value)

    def __copy__(self):
        return BigInt(self)

    def __int__(self) -> int:
        return int(self.__repr)

    def __int64__(self) -> np.int64:
        return self.__repr

    def __add__(self, other):
        return BigInt(self.__repr + np.int64(other))

    def __mul__(self, other : (int, np.int32, np.int64, BigInt)):
        if isinstance(other, BigInt):
            _value = other.value
        else:
            _value = factor(other)

        _new = self.__copy__()
        for k, v in _value.items():
            _new.value[k] = _new.value.get(k, np.int64(0)) + v

        _new.update()
        return _new

    def __floordiv__(self, other):
        if isinstance(other, BigInt):
            _value = other.value
        else:
            _value = factor(other)

        _new = self.__copy__()
        for k, v in _value.items():
            _new.value[k] = _new.value.get(k, np.int64(0)) - v

        _new.update()
        return _new


if __name__ == '__main__':
    print("text_format(string):")
    print('abc' + text_format('def', 'black', 'white', 'italic') + 'ghi')
    print()

    print("show(maze):")
    maze = np.random.randint(0, 2, 100, dtype=int).reshape((10, 10))
    start = (0, 0)
    end = (9, 9)
    path = [(0,0)]
    for i in range(1, 10):
        p = (i-1, i)
        maze[p] = 0
        path.append(p)
        p = (i, i)
        maze[p] = 0
        path.append(p)

    show(maze, start, end, path)


    a = BigInt(64)
    b = a + 5
    c = a * b

