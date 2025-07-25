# Advent of Code
year = 2020
day = 21

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    ingr = dict()
    allergens = dict()
    for line in text:
        ingredients, names = line[:-1].split(' (contains ')
        for i in ingredients.split():
            ingr[i] = ingr.get(i, 0) + 1
        ingredients = set(ingredients.split())
        for name in names.split(', '):
            if name not in allergens:
                allergens[name] = set(ingredients)
            else:
                allergens[name] &= set(ingredients)

    stack = []
    for a in allergens:
        if len(allergens[a]) == 1:
            stack.append(a)

    while stack:
        a = stack.pop(0)
        for i in allergens.keys():
            if i == a:
                continue
            if allergens[a] & allergens[i]:
                allergens[i] -= allergens[a]
                if len(allergens[i]) == 1:
                    stack.append(i)

    allergen_names = [x for y in allergens.values() for x in y]

    pone = sum(ingr[x] for x in ingr if x not in allergen_names)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = ','.join([y for x in sorted(allergens.keys()) for y in allergens[x]])
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
