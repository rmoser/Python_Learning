# Advent of Code
year = 2017
day = 22

import numpy as np
import aocd
import utils

text0 = """
..#
#..
...
"""
text1 = aocd.get_data(day=day, year=year)

show = False


def run(arr, pos, iters, pone=True):
    _arr = arr.copy()

    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    direction = 0
    count = 0

    CLEAN = 0
    WEAKENED = 1
    FLAGGED = 2
    INFECTED = 3

    if not pone:
        _arr = _arr * INFECTED

    if show:
        utils.show(_arr, tuple(pos))

    for i in range(iters):
        if i & 1023 == 0:
            print(f'\r{i}', end='')
        _pos = tuple(pos)
        if pone:
            if _arr[_pos]:
                direction = (direction + 1) % 4
            else:
                count += 1
                direction = (direction - 1) % 4
            _arr[_pos] = (not _arr[_pos]) * INFECTED
        else:
            if _arr[_pos] == CLEAN:
                direction = (direction - 1) % 4
                _arr[_pos] = WEAKENED
            elif _arr[_pos] == WEAKENED:
                # same direction
                _arr[_pos] = INFECTED
                count += 1
            elif _arr[_pos] == INFECTED:
                direction = (direction + 1) % 4
                _arr[_pos] = FLAGGED
            else:
                direction = (direction + 2) % 4
                _arr[_pos] = CLEAN

        pos += directions[direction]
        if ((0, 0) > pos).any() or (_arr.shape <= pos).any():
            # Expand map
            pad = 10
            _arr = np.pad(_arr, pad)
            pos += (pad, pad)

        if show:
            print('\n', i)
            utils.show(_arr, tuple(pos))

    return _arr, pos, count


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    arr = (np.array([list(s) for s in text]) == '#').astype(int)
    n = len(arr) // 2
    pos = np.array((n, n))

    _, _, pone = run(arr.copy(), pos.copy(), 10000)

    # pos = np.array((n, n))

    a, p, ptwo = run(arr.copy(), pos.copy(), 10000000, pone=False)
    
    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
