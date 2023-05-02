# Advent of Code
year = 2018
day = 2

import numpy as np
import aocd
import itertools

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)


def score(name):
    d = {c: name.count(c) for c in set(name)}
    return 2 in d.values(), 3 in d.values()


def comp(a, b):
    return sum(x != y for x, y in zip(a, b))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    scores = np.array([score(w) for w in text])
    pone = np.product(scores.sum(axis=0))

    for a, b in itertools.combinations(text, 2):
        if comp(a, b) == 1:
            ptwo = "".join([x for x, y in zip(a, b) if x == y])
            break


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
