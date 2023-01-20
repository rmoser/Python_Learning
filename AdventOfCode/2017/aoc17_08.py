# Advent of Code
year = 2017
day = 8

import numpy as np
import aocd

text0 = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""
text1 = aocd.get_data(day=day, year=year)


instructions = {
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
}


def run(program, reg=None):
    reg_max = 0

    debug = False
    if reg is None:
        reg = dict()

    for line in program:
        r, inst, x, _, a, comp, b = line.split()
        _r = reg.get(r, 0)
        _x = reg.get(x, 0) if x.isalpha() else int(x)
        _a = reg.get(a, 0) if a.isalpha() else int(a)
        _b = reg.get(b, 0) if b.isalpha() else int(b)

        if debug:
            print(line)
            print(_r, _x, _a, f"'{comp}'", _b)

        if inst == 'dec':
            _x *= -1

        f = instructions[comp]
        if f(_a, _b):
            reg[r] = _r + _x
            if debug:
                print(True, reg[r])
        else:
            reg[r] = _r
            if debug:
                print(False, reg[r])

        reg_max = max(reg_max, *reg.values())
    return max(reg.values()), reg_max


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    program = text.strip().splitlines()

    reg = dict()
    pone, ptwo = run(program, reg)




    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
