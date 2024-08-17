# Advent of Code
year = 2023
day = 9

import numpy as np
import aocd

text0 = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
text1 = aocd.get_data(day=day, year=year)

def predict(s):
    deltas = [a-b for a, b in zip(s[1:], s[:-1])]
    if all([d==0 for d in deltas]):
        return s + [s[-1]]
    else:
        return s + [s[-1] + predict(deltas)[-1]]

def edict(s):
    deltas = [a-b for a, b in zip(s[1:], s[:-1])]
    if all([d==0 for d in deltas]):
        return [s[0]] + s
    else:
        return [s[0] - edict(deltas)[0]] + s


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    data = []
    for line in text:
        data.append([int(i) for i in line.split()])

    pone = sum([predict(d)[-1] for d in data])
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = sum([edict(d)[0] for d in data])
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
