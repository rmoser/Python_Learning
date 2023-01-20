# Advent of Code
year = 2021
day = 25

import numpy as np
import aocd

text0 = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
text1 = aocd.get_data(day=day, year=year)


def east(arr):
    return np.append(arr[:,1:], arr[:,0:1], axis=1)

def west(arr):
    return np.append(arr[:,-1:], arr[:,:-1], axis=1)

def south(arr):
    return np.append(arr[1:,:], arr[0:1,:], axis=0)

def north(arr):
    return np.append(arr[-1:,:], arr[:-1,:], axis=0)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    arr = np.array([list(x) for x in text])

    iters = 0
    arrs = [arr]

    while True:
        iters += 1
        moves_east = np.bitwise_and(arr == '>', east(arr) == '.')

        _arr = arr.copy()
        _arr[moves_east] = '.'
        _arr[west(moves_east)] = '>'

        moves_south = np.bitwise_and(_arr == 'v', south(_arr) == '.')
        _arr[moves_south] = '.'
        _arr[north(moves_south)] = 'v'

        arrs.append(_arr)
        # print(iters, '\n', _arr)

        # print("Moves: ", (arr != _arr).sum())

        if (_arr == arr).all():
            break

        arr = _arr

    pone = iters

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
