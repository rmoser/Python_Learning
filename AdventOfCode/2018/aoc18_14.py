# Advent of Code
year = 2018
day = 14

import numpy as np
import aocd
from collections import deque

text0 = """9"""
text1 = aocd.get_data(day=day, year=year)


def run(n):
    global recipes, p0, p1, r
    if n < len(recipes):
        n += len(recipes) - 10

    while len(recipes) < n + 10:
        _ = [recipes.append(int(x)) for x in list(str(int(recipes[p0]) + int(recipes[p1])))]
        p0 = (p0 + int(recipes[p0]) + 1) % len(recipes)
        p1 = (p1 + int(recipes[p1]) + 1) % len(recipes)

    r = ''.join(np.array(recipes).astype(str))


def score(n):
    global recipes, p0, p1
    if n > len(recipes):
        run(n+10)
    return r[n:n + 10]


def find(substring, loops=np.inf):
    global recipes, p0, p1, r

    substring = str(substring)
    n = len(substring)

    return r.find(substring)

    # if i >= 0:
    #     return i

    # while substring not in recipes[-1000000-n-1:]:
    #     run(1000000)
    #     loops -= 1
    #     if loops <= 0:
    #         return None
    #
    # return recipes.find(substring)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    text = int(text)

    recipes = [3, 7]
    r = '37'
    p0 = 0
    p1 = 1

    run(25000000)

    pone = score(text)

    pone = r[text:text+10]
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = find(text)
    # if result is None:

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
