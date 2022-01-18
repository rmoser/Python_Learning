# Advent of Code
year = 2016
day = 25

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)


def run(program, reg):
    debug = False
    i = 0  # Init

    while True:
        # print(i, len(text))
        if 0 > i or i >= len(text):
            print("Broke at: ", i)
            break

        line = text[i]
        inst, a, b = (line.split() + [''])[:3]

        if debug:
            print(i, inst, a, b, reg)

        if inst == 'cpy':
            reg[b] = reg[a] if a in 'abcd' else int(a)
        elif inst == 'inc':
            reg[a] += 1
        elif inst == 'dec':
            reg[a] -= 1
        elif inst == 'jnz':
            a = reg[a] if a in 'abcd' else int(a)
            # print('jnz a:', a)
            if a != 0:
                i += reg[b] if b in 'abcd' else int(b)
                # print("jnz: ", i)
                continue
        elif inst == 'out':
            print(i, "out: ", reg[a] if a in 'abcd' else int(a), reg)

        i += 1

    return reg


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    # reg = run(text, {'a': 158, 'b': 0, 'c': 0, 'd': 0})

    # When dividing by 2, each successive value must alternate between even and odd...
    x = 0
    for i in range(15):
        if i & 1 == 0:
            x += 1
        x *= 2
        print(i, x)

    # The the code adds 2572, and the next higher integer with the correct even/odd property is 2730
    # reg['d'] = reg['a'] + 643 * 4
    # text = text[]
    pone = 158
    print(f"AOC {year} day {day}  Part One: {pone}")

    exit(0)

    ptwo = reg['a']
    print(f"AOC {year} day {day}  Part Two: {ptwo}")