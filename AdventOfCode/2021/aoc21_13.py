# Advent of Code
year = 2021
day = 13

import numpy as np
import aocd

np.printoptions.linewidth = 500

text0 = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
text1 = aocd.get_data(day=day, year=year)


def fold(paper, instruction):
    axis, n = instruction

    if axis == 'y':
        half0 = paper[:n, :]
        half1 = np.flipud(paper[n+1:, :])
        return half0 | half1

    half0 = paper[:, :n]
    half1 = np.fliplr(paper[:, n+1:])
    return half0 | half1


def print_paper(paper):
    for row in paper:
        s = ''.join(row.astype(int).astype(str))
        print(s.translate(s.maketrans('01', ' ' + chr(9608))))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    coords = []
    insts = []
    for line in text:
        if "," in line:
            a, b = line.split(",")
            coords.append((int(b), int(a))) # y=row, x=col
        elif 'fold' in line:
            axis, n = line.split()[-1].split("=")
            insts.append((axis, int(n)))
    coords = tuple(coords)

    x_max = max([c[1] for c in coords])
    y_max = max([c[0] for c in coords])

    paper = np.zeros(shape=(y_max+1, x_max+1), dtype=np.bool)

    for c in coords:
        paper[c] = 1

    # print_paper(paper)

    new = fold(paper, insts[0])

    # print_paper(new)

    # print(insts)
    # print(y_max, x_max)

    pone = new.sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    for inst in insts:
        paper = fold(paper, inst)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")

    print_paper(paper)

