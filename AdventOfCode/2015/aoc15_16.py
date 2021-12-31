# Advent of Code
year = 2015
day = 16

import numpy as np
import aocd

text0 = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    clue = dict()
    for line in text:
        s = line.split(':')
        clue[s[0]] = int(s[1])

    text = text1
    text = text.strip().splitlines()

    aunts = [dict()]
    for line in text:
        line = line.replace(':', '').replace(',', '')
        s = line.split()
        d = dict()

        c = s[2]
        v = s[3]
        d[c] = int(v)

        c = s[4]
        v = s[5]
        d[c] = int(v)

        c = s[6]
        v = s[7]
        d[c] = int(v)

        aunts.append(d)

    print(len(aunts))

    for i, aunt in enumerate(aunts):
        if len(aunt) == 0:
            continue

        result = True
        for k, v in aunt.items():
            if k in clue:
                if clue[k] != v:
                    result = False
                    break

        if result:
            pone = i
            print(f"Sue {i}: {aunt}")
            break

    for i, aunt in enumerate(aunts):
        if len(aunt) == 0:
            continue

        result = True
        for k, v in aunt.items():
            if k in clue:
                if k in ('cats', 'trees'):
                    if clue[k] >= v:
                        result = False
                        break
                elif k in ('goldfish', 'pomeranians'):
                    if clue[k] <= v:
                        result = False
                        break
                elif clue[k] != v:
                    result = False
                    break

        if result:
            ptwo = i
            print(f"Sue {i}: {aunt}")
            break

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
