# Advent of Code
year = 2024
day = 1

import numpy as np
import aocd
import os
import numpy as np

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
3   4
4   3
2   5
1   3
3   9
3   3
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    a = list()
    b = list()

    for line in text:
        i, j = line.split()
        a.append(int(i))
        b.append(int(j))

    a = np.array(sorted(a))
    b = np.array(sorted(b))

    pone = np.abs(a-b).sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = 0
    for i in a:
        ptwo += i * (b == i).sum()

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
