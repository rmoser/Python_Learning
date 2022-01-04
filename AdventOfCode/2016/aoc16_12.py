# Advent of Code
year = 2016
day = 12

import numpy as np
import aocd

text0 = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""
text1 = aocd.get_data(day=day, year=year)


def run(program, reg):
    i = 0  # Init
    while True:
        # print(i, len(text))
        if 0 > i or i >= len(text):
            break

        line = text[i]
        inst, a, b = (line.split() + [''])[:3]
        if inst == 'cpy':
            reg[b] = reg[a] if a in 'abcd' else int(a)
        elif inst == 'inc':
            reg[a] += 1
        elif inst == 'dec':
            reg[a] -= 1
        else:
            a = reg[a] if a in 'abcd' else int(a)
            if a != 0:
                i += reg[b] if b in 'abcd' else int(b)
                continue

        i += 1

    return reg


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    reg = run(text, {'a': 0, 'b': 0, 'c': 0, 'd': 0})
    pone = reg['a']
    print(f"AOC {year} day {day}  Part One: {pone}")


    reg = run(text, {'a': 0, 'b': 0, 'c': 1, 'd': 0})
    ptwo = reg['a']
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
