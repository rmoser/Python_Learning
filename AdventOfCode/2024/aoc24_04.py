# Advent of Code
year = 2024
day = 4

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
text1 = aocd.get_data(day=day, year=year)

def check(array, word="XMAS"):
    arr = array.copy()
    length = len(word)-1
    result = 0

    for _ in range(4):
        rows = arr.shape[0]
        cols = arr.shape[1]

        if length <= cols:
            horizontal = np.ones((arr.shape[0], arr.shape[1]-length), dtype=bool)
        else:
            horizontal = np.array([False])

        if length <= rows and length <= cols:
            diagonal = np.ones((arr.shape[0]-length, arr.shape[1]-length), dtype=bool)
        else:
            diagonal = np.array([False])

        for i, c in enumerate(word):
            if horizontal.any():
                a = arr[:, i:i+cols-length]
                horizontal = np.bitwise_and(horizontal, a == word[i])

            if diagonal.any():
                a = arr[i:i+rows-length, i:i+cols-length]
                diagonal = np.bitwise_and(diagonal, a == word[i])

        result += horizontal.sum() + diagonal.sum()
        arr = np.rot90(arr)

    return result


def check2(array):
    arr = array.copy()
    length = 2
    result = 0

    for _ in range(4):
        rows = arr.shape[0]
        cols = arr.shape[1]

        if length <= cols and length <= rows:
            match = np.ones((arr.shape[0]-length, arr.shape[1]-length), dtype=bool)
        else:
            match = np.array([False])


        a = arr[1:-1, 1:-1] == 'A'
        m0 = arr[:-2, :-2] == 'M'
        m1 = arr[2:, :-2] == 'M'
        s0 = arr[:-2, 2:] == 'S'
        s1 = arr[2:, 2:] == 'S'

        match = a * m0 * m1 * s0 * s1
        result += match.sum()
        arr = np.rot90(arr)

    return result

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    word = 'XMAS'

    text = text1
    text = text.strip().splitlines()

    arr = np.array([list(line) for line in text])

    pone = check(arr)
    ptwo = check2(arr)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
