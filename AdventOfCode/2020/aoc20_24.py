# Advent of Code
year = 2020
day = 24

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import collections

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""
text1 = aocd.get_data(day=day, year=year)

def parse(line):
    steps = []
    while line:
        if line[0] in 'ns':
            steps.append(line[:2])
            line = line[2:]
            continue
        if line[0] in 'ew':
            steps.append(line[0])
            line = line[1:]
    return steps

DIRS = {
    'ne': (1, 1),
    'nw': (1, -1),
    'se': (-1, 1),
    'sw': (-1, -1),
    'e': (0, 2),
    'w': (0, -2)
}

def run(tiles):
    to_check = set(tiles.keys())
    counts = collections.defaultdict(int)

    for tile in tiles:
        pos = np.array(tile)
        to_check |= (set(tuple((pos + d).tolist()) for d in DIRS.values()))

    for tile in to_check:
        pos = np.array(tile)
        check = sum(tiles[tuple((pos + d).tolist())] for d in DIRS.values())
        counts[tile] = check

    for tile in counts:
        # Black tile
        if tiles[tile] == 1:
            if counts[tile] == 0 or counts[tile] > 2:
                tiles[tile] = 0
            continue

        # White tile
        if counts[tile] == 2:
            tiles[tile] = 1

    for tile in list(tiles.keys()):
        if not tiles[tile]:
            del tiles[tile]

    return tiles

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    tiles = collections.defaultdict(int)

    text = text1
    text = text.strip().splitlines()

    steps = [parse(line) for line in text]

    for path in steps:
        pos = np.array([0, 0])
        for d in path:
            pos += DIRS[d]

        pos = tuple(pos.tolist())
        tiles[pos] = 1 - tiles[pos]
        if not tiles[pos]:
            del tiles[pos]

    pone = sum(tiles.values())

    print(f"AOC {year} day {day}  Part One: {pone}")

    for _ in range(100):
        tiles = run(tiles)

    ptwo = len(tiles)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
