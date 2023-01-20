# Advent of Code
year = 2022
day = 3

import numpy as np
import aocd

text0 = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
text1 = aocd.get_data(day=day, year=year)


def priority(c):
    o = ord(c)
    if o > 90:
        o -= 96
    else:
        o -= 38
    return o


def sacks(text):
    t = []
    for x in text:
        l = len(x) // 2
        t.append((x[:l], x[l:]))
    return t


def groups(text):
    g = []
    for i in range(0, len(text), 3):
        g.append(text[i:i+3])
    return g


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    s = sacks(text)

    pone = sum((priority((set(a) & set(b)).pop()) for a, b in s))

    g = groups(text)
    ptwo = sum((priority((set(a) & set(b) & set(c)).pop()) for a, b, c in g))

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
