# Advent of Code
year = 2022
day = 2

import numpy as np
import aocd

text0 = """
A Y
B X
C Z
"""
text1 = aocd.get_data(day=day, year=year)


def score(rnd):
    scores = {'X': 1, 'Y': 2, 'Z': 3}
    a, b = rnd
    s = scores[b]
    if rnd in (('A', 'X'), ('B', 'Y'), ('C', 'Z')):
        s += 3
    elif rnd in (('A', 'Y'), ('B', 'Z'), ('C', 'X')):
        s += 6
    return s


def score2(rnd):
    draw = {'A': 'X', 'B': 'Y', 'C': 'Z'}
    win = {'A': 'Y', 'B': 'Z', 'C': 'X'}
    lose = {'A': 'Z', 'B': 'X', 'C': 'Y'}
    scores = {'X': 1, 'Y': 2, 'Z': 3}
    a, b = rnd

    if b == 'X':
        b = lose[a]
    elif b == 'Y':
        b = draw[a]
    elif b == 'Z':
        b = win[a]
    rnd = a, b

    s = scores[b]
    if rnd in (('A', 'X'), ('B', 'Y'), ('C', 'Z')):
        s += 3
    elif rnd in (('A', 'Y'), ('B', 'Z'), ('C', 'X')):
        s += 6
    return s


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = [tuple(x.split()) for x in text.strip().splitlines()]

    game = [score(x) for x in text]

    pone = sum(game)

    print(f"AOC {year} day {day}  Part One: {pone}")

    game2 = [score2(x) for x in text]
    ptwo = sum(game2)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
