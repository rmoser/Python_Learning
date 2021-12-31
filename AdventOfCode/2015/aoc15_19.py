# Advent of Code
year = 2015
day = 19

import numpy as np
import aocd

text0 = """
e => H
e => O
H => HO
H => OH
O => HH
"""
text1 = aocd.get_data(day=day, year=year)


def deconstruct(word, d, n=0):
    if word in d['e']:
        return 'e', n+1

    matched = False

    print(word)

    for k, vals in d.items():
        if k == 'e':
            continue
        for v in vals:
            print(v, end='..')
            count = word.count(v)
            if count:
                    matched = True
                    word = word.replace(v, k)
                    n += count

    print()

    if matched:
        return deconstruct(word, d, n)

    return word, n


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    words = []
    d = dict()
    molecule = ''
    for line in text:
        if ' => ' in line:
            k, v = line.split(' => ')
            if k not in d:
                d[k] = []
            d[k].append(v)
            continue

        if len(line):
            molecule += line

    if len(molecule) == 0:
        molecule = 'HOH'

    print(molecule, len(molecule))

    for i, c in enumerate(molecule):
        if c in d:
            left, right = molecule[0:i], molecule[min(len(molecule), i+1):]
            for ins in d[c]:
                # print(f"i {i}, c {c}, '{left}' '{ins}' '{right}'")
                words.append(left + ins + right)

    for i, c in enumerate(molecule):
        c = molecule[i:i+2]
        if c in d:
            left, right = molecule[0:i], molecule[min(len(molecule), i+2):]
            for ins in d[c]:
                # print(f"i {i}, c {c}, '{left}' '{ins}' '{right}'")
                words.append(left + ins + right)

    words = np.unique(words)
    pone = len(words)

    print(f"AOC {year} day {day}  Part One: {pone}")

    word, n = deconstruct(molecule, d)

    ptwo = n
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
