# Advent of Code
year = 2020
day = 20

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import math
import scipy as sp

utils.DEFAULT_TRANSLATE[ord('2')] = ord('o')

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""
text1 = aocd.get_data(day=day, year=year)

DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))
PICS = dict()
POS = dict()
DONE = set()
PICTURE = None
MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

def find_monster():
    monster = (np.array([list(x) for x in MONSTER.splitlines()]) == '#').astype(int)
    _monster = monster[::-1]  # Flipped vertically
    arr = PICTURE.copy()

    monsters = set()
    s = monster.shape
    rows = tuple(range(arr.shape[0] - monster.shape[0] + 1))
    cols = tuple(range(arr.shape[1] - monster.shape[1] + 1))
    match = monster.sum()
    for _ in range(4):
        for r in rows:
            for c in cols:
                # print(r, ':', r+s[0], ', ', c, ':', c+s[1])
                sub_arr = arr[r:r+s[0], c:c+s[1]]

                prod = (sub_arr * monster) > 0
                if prod.sum() >= match:
                    sub_arr[prod > 0] = 2
                    m = np.array(np.where(prod))
                    m[0] += r
                    m[1] += c
                    monsters |= set([tuple(x) for x in m.T.tolist()])

                prod = (sub_arr * _monster) > 0
                if prod.sum() >= match:
                    sub_arr[prod > 0] = 2
                    m = np.array(np.where(prod))
                    m[0] += r
                    m[1] += c
                    monsters |= set([tuple(x) for x in m.T.tolist()])

        arr = np.rot90(arr, 1)
    if monsters:
        PICTURE[:,:] = arr


def shrink():
    global PICTURE
    drop_rows = np.array(range(0, PICTURE.shape[0], 10))
    drop_rows = tuple(drop_rows) + tuple(drop_rows - 1)

    drop_cols = np.array(range(0, PICTURE.shape[1], 10))
    drop_cols = tuple(drop_cols) + tuple(drop_cols - 1)

    arr = np.delete(PICTURE, drop_rows, axis=0)
    arr = np.delete(arr, drop_cols, axis=1)

    PICTURE = arr.copy()

def sides(arr):
    # N E S W  with values for each side ordered clockwise
    return arr[0,:], arr[:,-1], arr[-1,::-1], arr[::-1,0]

def all_rots(arr):
    s = np.array(sides(arr))
    r = s[:,::-1]
    return np.concatenate((s, r))

def rot(arr, n):
    # Rotate to align as if side n matched the top row in normal order (increasing to the right)
    match n:
        case 0:
            return arr[::-1, :]
        case 1:
            return arr.T
        case 2:
            return arr[:, ::-1]  # Flip horizontal
        case 3:
            return np.rot90(arr, 1)[:, ::-1]
        case 4:
            return np.rot90(arr, 2)
        case 5:
            return np.rot90(arr, -1)  # Rotate Right 90
        case 6:
            return arr
        case 7:
            return np.rot90(arr)

def can_connect(a, b):
    if isinstance(a, int) and a in PICS:
        a = PICS[a]
    if isinstance(b, int) and b in PICS:
        b = PICS[b]

    # N E S W
    a_sides = sides(a)
    b_sides = all_rots(b)

    result = []
    for i, a_side in enumerate(a_sides):
        m = (a_side == b_sides).all(axis=1)
        if m.any():
            result.append((i, np.where(m)[0].tolist()))
    return result

def get_array_coords(pic):
    shape = np.array(PICS[pic].shape)
    return tuple((POS[pic][0] * shape).tolist())

def write(tile, pos):
    arr = PICS[tile]
    # print(tile, pos, arr.shape)
    s = arr.shape
    pos = np.array(pos)
    PICTURE[pos[0]*s[0]:(pos[0]+1)*s[0], pos[1]*s[1]:(pos[1]+1)*s[1]] = arr
    POS[tile] = tuple(pos.tolist())
    POS[tuple(pos.tolist())] = tile

def hist(connections):
    d = dict()
    for v in connections.values():
        d[len(v)] = d.get(len(v), 0) + 1
    pprint(d)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n')

    for page in text:
        page = page.splitlines()
        tile = int(page[0][-5:-1])
        arr = (np.array([list(x) for x in page[1:]]) == '#').astype(int)
        PICS[tile] = arr

    s = np.array(arr.shape)
    PICTURE = np.zeros(s * int(math.sqrt(len(PICS))), dtype=int)

    # Identify which tiles can connect
    connections = dict()
    for a, b in it.permutations(PICS.keys(), 2):
        x = can_connect(PICS[a], PICS[b])
        if x:
            if a not in connections:
                connections[a] = []
            connections[a].append(b)
            # print(a, b, can_connect(PICS[a], PICS[b]))

    pone = math.prod(c for c in connections if len(connections[c]) == 2)

    print(f"AOC {year} day {day}  Part One: {pone}")

    # Assemble the picture
    # Pick a corner tile to be the upper left
    upper_left_tile = min(c for c in connections if len(connections[c]) == 2)


    needed_sides = set([can_connect(upper_left_tile, x)[0][0] for x in connections[upper_left_tile]])

    # Rotate so that the connecting sides will face the open area of the picture
    if needed_sides == {0, 1}:
        PICS[upper_left_tile] = np.rot90(PICS[upper_left_tile], 3)
    elif needed_sides == {1, 2}:
        pass
    elif needed_sides == {2, 3}:
        PICS[upper_left_tile] = np.rot90(PICS[upper_left_tile], 1)
    elif needed_sides == {0, 3}:
        PICS[upper_left_tile] = np.rot90(PICS[upper_left_tile], 2)

    path = [x for x in it.product(range(120), range(120)) if (x[0] % 10) in (0, 9) or (x[1] % 10) in (0, 9)]

    # picture[:s[0], :s[1]] = PICS[upper_left_tile]
    PICTURE[:,:] = 0
    POS.clear()
    write(upper_left_tile, (0, 0))
    DONE.clear()
    stack = [upper_left_tile]
    while stack:
        # print(len(stack), len(DONE))
        a = stack.pop(0)
        if a not in DONE:
            for b in connections[a]:
                # if a == 2999 and b == 1619:
                #     input(' ')
                if b in POS:
                    continue
                pos = np.array(POS[a])
                new = pos.copy()
                [(side, [rotation])] = can_connect(a, b)
                PICS[b] = np.rot90(rot(PICS[b], rotation), -side)
                pos = (pos + DIRS[side])
                if tuple(pos) in POS.values():
                    raise(Exception(f'Tile assembly error: {a} -> {b} on {side}'))

                if np.bitwise_and(pos >= 0, pos < np.array(PICTURE.shape) // s).all():
                    write(b, pos)
                    stack.append(b)
                else:
                    print(f'Missed tile: {b}')
                # print(f'a: {a}, b: {b}, side: {side}, rot: {rotation}, pos: {pos}')

        DONE.add(a)

    if False:
        tile_pos = list(tuple(x) for x in np.array(list(it.product(range(1, 9), range(1, 9)))) + np.array(POS[a])*10)
        utils.show(PICTURE, path=path)

    shrink()

    # utils.show(PICTURE)
    PICTURE = np.rot90(PICTURE, 2)
    find_monster()
    PICTURE = np.rot90(PICTURE, 1)
    path = (tuple(x) for x in np.array(np.where(PICTURE==2)).T.tolist())
    utils.show(PICTURE, path=path)

    ptwo = (PICTURE == 1).sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")

