# Advent of Code
year = 2024
day = 18

import numpy as np
import aocd
import os
import utils
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    if text == text0:
        size = 7
        n = 12
    else:
        size = 71
        n = 1024
    text = text.strip().splitlines()


    arr = np.zeros(shape=(size, size), dtype=int)
    start = (0, 0)
    end = (np.array(arr.shape) - 1).tolist()

    arr = np.zeros(shape=(size, size), dtype=int)
    for i, line in enumerate(text):
        c, r  = [int(j) for j in line.split(',')]
        arr[(r, c)] = True

        if i == n-1:
            x = utils.valid_path(arr, start=start, end=end)
            pone = len(x[0]) - 1
            continue

        if i > n:
            if (r, c) in x[0]:
                x = utils.valid_path(arr, start=start, end=end, iters=n**2)
                if not x[0]:
                    ptwo = line
                    break

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
