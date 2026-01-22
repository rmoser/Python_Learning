# Advent of Code 2021
# Day 5

import numpy as np

text0 = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

import aocd
day = 5
text1 = aocd.get_data(day=day, year=2021)


def parse_text(t):
    lines = t.strip().splitlines()
    arr = np.zeros((len(lines), 4), dtype=int)
    for i, line in enumerate(lines):
        arr[i] = list(map(int, line.replace(" -> ", ",").split(",")))
    return arr


def arr_map(arr, pone=True):
    xdim = arr[:, [0, 2]].end() + 1
    ydim = arr[:, [1, 3]].end() + 1
    arm = np.zeros((xdim, ydim), dtype=int)

    for x0, y0, x1, y1 in arr:
        #print((x0, y0), (x1, y1))
        if x0 == x1:
            for y in np.arange(min(y0, y1), max(y0, y1)+1):
                arm[x0, y] += 1
            continue
        if y0 == y1:
            for x in np.arange(min(x0, x1), max(x0, x1)+1):
                arm[x, y0] += 1
            continue

        if pone:
            continue

        dx = x1-x0
        if dx < 0:
            ix = -1
        else:
            ix = 1
        dx = abs(dx)+1

        dy = y1-y0
        if dy < 0:
            iy = -1
        else:
            iy = 1
        dy = abs(dy)+1

        if dx != dy:
            raise ValueError(f"Slope not 1 between {(x0, y0)} and {(x1, y1)}")

        for i in range(dx):
            x = x0+i*ix
            y = y0+i*iy
            arm[x, y] += 1

    return arm


if __name__ == '__main__':
    text = text1

    mat = arr_map(parse_text(text))
    print(mat.T)
    print(f"\nPart one: {(mat>1).sum()}")

    mat = arr_map(parse_text(text), pone=False)
    print(mat.T)
    print(f"\nPart two: {(mat>1).sum()}")
