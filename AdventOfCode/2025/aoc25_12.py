# Advent of Code
from sympy import false

year = 2025
day = 12

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic
import scipy as sp
import itertools as it

text0 = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
text1 = aocd.get_data(day=day, year=year)

tiles = []
tile_map = {}
tile_map_reverse = {}
tile_map_array = None

def init_tiles(boxes):
    global tiles, tile_map, tile_map_array
    tiles = []
    tile_map = {}
    for box, tile in boxes.items():
        tile_map[box] = set()
        for _ in range(4):
            for t in (tile, np.fliplr(tile)):
                if not arr_in_list(t, tiles):
                    tiles.append(t)
                    tile_map[box].add(len(tiles) - 1)
                    tile_map_reverse[len(tiles) - 1] = box
            tile = np.rot90(tile)

    tile_map_array = np.zeros((len(tiles), len(boxes)), dtype=int)
    for b in range(len(boxes)):
        for t in tile_map[b]:
            tile_map_array[t, b] = 1

    return tiles, tile_map, tile_map_array

def init_arr(size=None, tree=None, dtype=np.int8):
    if size is None and tree is None:
        raise ValueError('size or tree must be specified')
    elif tree is not None:
        size = sum(tree[1]), tree[0][0]-2, tree[0][1]-2
    return np.full(size, dtype=dtype, fill_value=-1)

def arr_in_list(arr, list):
    return any((a==arr).all() for a in list)

def box_count(arr):
    counts = np.bincount(arr[np.bitwise_and(0 <= arr, arr<=tile_map_array.shape[0])], minlength=tile_map_array.shape[0])
    return tuple(counts.dot(tile_map_array).tolist())

def is_valid(arr):
    # All values between 0 and num(tiles), inclusive
    if not (-1 <= arr.min() <= arr.max() <= tile_map_array.shape[0]):
        return False

    # Only one tile per coordinate
    _arr = calculate_placements(arr)
    if not (_arr.sum(axis=0) <= 1).all():
        return False  # Tiles overlap

    return True


def is_solution(arr, tree):
    if not is_valid(arr):
        return False
    answer = np.array(tree[1])
    total = box_count(arr)
    if not len(total) == answer.shape[0]:
        return False
    return (total == answer).all()


def calculate_placements(arr):
    size = (np.array(arr.shape) + (0, 2, 2)).tolist()
    _arr = init_arr(size)

    for i, row in enumerate(arr):
        tile_num = row.max()
        if tile_num <= tile_map_array.shape[0]:
            _arr[i] = sp.signal.convolve(row>=0, tiles[tile_num])
    return _arr

def display_placements(arr):
    for i in np.array(list(zip(*np.where(arr)))).tolist():
        print(i, ":", arr[tuple(i)])


def next_box(arr, tree):
    remaining = box_count(arr) - tree[1]
    return (remaining > 0).argmax()


def solve_tree(tree):
    # Valid area for placements is 2 less, since each tile is 3x3
    size = tuple((np.array(tree[0]) - 2).tolist())

    _box_count = sum(tree[1])  # Total number of boxes required for solution

    # Box placement array has one row for each box to place
    arr = init_arr((_box_count, ) + size)

    _solve_tree(arr, tree)

    if is_solution(arr, tree):
        return tuple(box_count(arr).tolist())
    else:
        return tuple()


def _solve_tree(arr, tree):
    # Simple flow:
    # 1. If no more tiles need to be placed, return True
    # 2. Find the next open row and next tile to place
    # 3. Loop through all valid placements, updating arr[row]
    # 4.    Recursive call to self on arr
    # 5. If we ran out of valid placements, return False
    # Return the value of the recursive call

    tile_count = len(tiles)
    _box_count = sum(tree[1])  # Total number of boxes required for solution

    nonempty_rows = np.where(arr)[0]
    row = (nonempty_rows.argmax()+1) if nonempty_rows.size else 0

    for t in range(tile_count):
        row[t] = 1


    for tile_num in range(len(tiles)):
        for t in tile_map[tile_num]:
            for iter_set in it.product(range(tile_count)):
                pass

    while True:
        pass
        break


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().split('\n\n')

    trees = text[-1].splitlines()
    for i, v in enumerate(trees):
        trees[i] = v.split(': ')
        trees[i][0] = tuple((int(x) for x in trees[i][0].split('x')))
        trees[i][1] = tuple((int(x) for x in trees[i][1].split()))


    boxes = dict()
    for box in text[:-1]:
        k = int(box.split(':')[0])
        v = (np.array([list(line) for line in box.splitlines()[1:]]) == '#').astype(int)
        boxes[k] = v
        # v = (np.array([list(line) for line in box.splitlines()[1:]]) == '#').astype(int)
        # boxes[k] = list(zip(*np.array(np.where(v)).tolist()))

    init_tiles(boxes)

    tile_arr = np.array(tiles, dtype=int)

    tree = trees[0]
    arr = init_arr(tree=tree)
    arr[0,0,0] = 22
    arr[1,1,1] = 23

    ic(is_valid(arr))
    ic(is_solution(arr, tree))



    #
    # To place boxes based on locator values:
    # sp.signal.convolve(arr[4], tile_arr[4], mode='full')[:4,:4]

    # for dims, contents in trees:
        # area_available = dims[0] * dims[1]
        # area_needed = sum([boxes[i].sum() * t for i, t in enumerate(contents)])
        # if area_available > area_needed:
        #     ic(f'Space available: {area_available}, needed: {area_needed}')


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
