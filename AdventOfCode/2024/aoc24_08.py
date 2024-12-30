# Advent of Code
year = 2024
day = 8

import numpy as np
import aocd
import os
import utils
import itertools as it

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    array = np.array([list(line) for line in text])

    antinodes = set()
    antinodes2 = set()

    symbols = set(array[array != '.'])
    for symbol in symbols:
        nodes = np.array(np.where(array == symbol)).transpose()

        for a, b in it.combinations(nodes, 2):
            # Part one
            delta = b - a
            anti_a = a - delta
            if (anti_a >= 0).all() and (anti_a < array.shape).all():
                antinodes.add(tuple([int(x) for x in anti_a]))

            # Part two
            antinodes2.add(tuple([int(x) for x in a]))
            antinodes2.add(tuple([int(x) for x in b]))
            d = 1
            while (anti_a >= 0).all() and (anti_a < array.shape).all():
                antinodes2.add(tuple([int(x) for x in anti_a]))
                d += 1
                anti_a = a - d * delta

            anti_b = b + delta
            if (anti_b >= 0).all() and (anti_b < array.shape).all():
                antinodes.add(tuple([int(x) for x in anti_b]))

            d = 1
            while (anti_b >= 0).all() and (anti_b < array.shape).all():
                antinodes2.add(tuple([int(x) for x in anti_b]))
                d += 1
                anti_b = b + d * delta

    utils.show(array, path=antinodes2)

    pone = len(antinodes)
    ptwo = len(antinodes2)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
