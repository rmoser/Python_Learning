# Advent of Code
year = 2022
day = 4

import numpy as np
import aocd

text0 = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    t = [x.split(',') for x in text]
    for i, x in enumerate(t):
        t[i] = [tuple(int(z) for z in y.split('-')) for y in x]

    r = list(range(10))
    pone = 0
    ptwo = 0
    for p in t:
        a, b = p
        a = set(range(a[0], a[1]+1))
        b = set(range(b[0], b[1]+1))
        # print(a, b, a-b, b-a)
        if not(a - b) or not(b - a):
            pone += 1
        if a & b:
            ptwo += 1

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
