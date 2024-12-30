# Advent of Code
year = 2024
day = 19

import numpy as np
import aocd
import os
import functools
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
text1 = aocd.get_data(day=day, year=year)

@functools.cache
def possible(towel, patterns):
    result = 0

    for pattern in patterns:
        if towel.startswith(pattern):
            if towel == pattern:
                # print(f"Match {towel} {pattern}")
                result += 1
            else:
                # print(f'Drop {towel} {pattern} call possible({towel[len(pattern):]})')
                result += possible(towel[len(pattern):], patterns)

    return result

if __name__ == '__main__':
    text = text1
    text = text.strip()

    a, b = text.split('\n\n')

    patterns = tuple(a.split(', '))
    towels = b.splitlines()

    # print(possible(towels[0], patterns))
    pone = 0
    ptwo = 0
    for towel in towels:
        p = possible(towel, patterns)
        # print(towel, p)
        pone += p > 0
        ptwo += p

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
