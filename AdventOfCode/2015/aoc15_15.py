# Advent of Code
year = 2015
day = 15

import numpy as np
import aocd
import enum
import itertools

text0 = """ 
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""
text1 = aocd.get_data(day=day, year=year)


class Ingr(enum.IntEnum):
    capacity = 0
    durability = 1
    flavor = 2
    texture = 3
    calories = 4


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    d = dict()
    for line in text:
        s = line.split(':')
        name = s[0]
        params = s[1].split(", ")
        d[name] = [int(x.split()[-1]) for x in params]

    names = list(d.keys())
    values = np.array(list(d.values()))
    n = len(names)

    best_one = 0, [100, 0]
    best_two = 0, [100, 0]

    recipes = itertools.combinations_with_replacement(range(n), 100)
    for recipe in recipes:
        rec = np.array(recipe)
        ratios = [(rec == x).sum() for x in range(n)]

        score = (np.atleast_2d(ratios).T * values[:,:4]).sum(axis=0)
        score *= score > 0
        score = np.product(score)
        if score > best_one[0]:
            best_one = score, ratios

        calories = ((np.atleast_2d(ratios).T) * values[:, 4:5]).sum()
        if calories == 500 and score > best_two[0]:
            best_two = score, ratios

    pone = best_one[0]
    ptwo = best_two[0]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
