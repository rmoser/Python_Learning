# Advent of Code
year = 2015
day = 7

import numpy as np
import aocd

text0 = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

text1 = aocd.get_data(day=day, year=year)


def proc(ev, d):
    for tgt, src in d.items():

        if len(src.split()) == 1:
            if src.isnumeric():
                ev[tgt] = np.uint64(src)
                print(f"VAL Eval: {tgt} = {d[tgt]}: {ev[tgt]}")
            elif src in ev:
                ev[tgt] = ev[src]
                print(f"VA2 Eval: {tgt} = {d[tgt]}: {ev[tgt]}")
            continue

        if "NOT" in src:
            _, a = src.split()

            if a.isnumeric():
                a = np.uint16(a)
                ev[tgt] = np.bitwise_not(a)
                print(f"Eval: {tgt}")
            elif a in ev:
                a = ev[a]
                ev[tgt] = np.bitwise_not(a)
                print(f"NOT Eval: {tgt} = {d[tgt]}: {ev[tgt]}")
            continue

        print(f"{tgt} -> {src}")
        a, _, b = src.split()
        if a.isnumeric():
            a = np.uint16(a)
        elif a in ev:
            a = ev[a]
        else:
            continue
        if b.isnumeric():
            b = np.uint16(b)
        elif b in ev:
            b = ev[b]
        else:
            continue

        if "AND" in src:
            ev[tgt] = np.bitwise_and(a, b)
            print(f"AND Eval: {tgt} = {d[tgt]}: {ev[tgt]}")
            continue

        if "OR" in src:
            ev[tgt] = np.bitwise_or(a, b)
            print(f"OR  Eval: {tgt} = {d[tgt]}: {ev[tgt]}")
            continue

        if "LSHIFT" in src:
            ev[tgt] = a << b
            print(f"LSH Eval: {tgt} = {d[tgt]}: {ev[tgt]}")
            continue

        if "RSHIFT" in src:
            ev[tgt] = a >> b
            print(f"RSH Eval: {tgt} = {d[tgt]}: {ev[tgt]}")
            continue


    for k in ev:
        if k in d:
            d.pop(k)


if __name__ == '__main__':
    text = text1
    text = text.splitlines()

    d = dict()
    ev = dict()
    for line in text:
        if len(line) == 0:
            continue

        print(line)
        src, tgt = line.split(" -> ")

        if src.isnumeric():
            ev[tgt] = np.uint16(src)
            print(f"Eval: {tgt}")
            continue

        else:
            d[tgt] = src


    i = 0
    while 'a' in d:
        i += 1
        print(i, end='')
        proc(ev, d)

    print(f"AOC {year} day {day}  Part One: {ev['a']}")

    b = ev['a']

    d = dict()
    ev = dict()
    for line in text:
        if len(line) == 0:
            continue

        print(line)
        src, tgt = line.split(" -> ")

        if src.isnumeric():
            ev[tgt] = np.uint16(src)
            print(f"Eval: {tgt}")
            continue

        else:
            d[tgt] = src

    ev['b'] = b


    i = 0
    while 'a' in d:
        i += 1
        print(i, end='')
        proc(ev, d)

    print(f"AOC {year} day {day}  Part Two: {ev['a']}")
