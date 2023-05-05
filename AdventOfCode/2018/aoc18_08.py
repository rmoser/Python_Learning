# Advent of Code
year = 2018
day = 8

import numpy as np
import aocd

text0 = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"""
text1 = aocd.get_data(day=day, year=year)


def parse(l, d=None, parent=None):
    if not d:
        d = dict()
        i = 'A'
    else:
        i = chr(ord(max(d)) + 1)
    # print("Begin ", i, l, d)
    d[i] = [list(), list(), -1]

    if parent and parent in d:
        d[parent][0].append(i)

    c, m = l[0:2]
    l = l[2:]
    for _ in range(c):
        l, d = parse(l, d, i)
        # print(l, d)

    # print("Mid   ", i, l, d)

    d[i][1] = l[:m]
    l = l[m:]

    # Score = sum(Child node score for j in Metadata if Child node exists)
    if d[i][0]:  # Has child nodes
        d[i][2] = sum(d[d[i][0][j-1]][2] for j in d[i][1] if j <= len(d[i][0]))
    else:        # Has no child nodes
        d[i][2] = sum(d[i][1])

    # print("End   ", i, l, d)

    return l, d


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    recipes = [int(x) for x in text.split()]

    _, d = parse(recipes)

    pone = sum(sum(x[1]) for x in d.values())

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = d['A'][2]

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
