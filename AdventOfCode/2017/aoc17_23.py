# Advent of Code
year = 2017
day = 23

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)

debug = 2

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    reg = dict()
    for x in 'abcdefgh':
        reg[x] = 0

    i = 0
    mul_count = 0
    op_count = 0
    while i < len(text):
        inst, arg, val = text[i].split()

        _arg = reg[arg] if arg in reg else int(arg)
        _val = reg[val] if val in reg else int(val)

        op_count += 1

        inc = 1
        if inst == 'set':
            reg[arg] = _val
        elif inst == 'sub':
            reg[arg] = _arg - _val
        elif inst == 'mul':
            mul_count += 1
            reg[arg] = _arg * _val
        elif inst == 'jnz':
            if _arg != 0:
                inc = _val
        i += inc

        if debug == 2 or debug == 1 and (op_count & 1023 == 0):
            print(f"{op_count} {mul_count}\t\t{i}:{inst}  {arg}: {_arg}, {val}: {_val}, {reg}")

    pone = mul_count

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
