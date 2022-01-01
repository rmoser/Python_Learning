# Advent of Code
year = 2015
day = 23

import numpy as np
import aocd

text0 = """ 
inc a
jio a, +2
tpl a
inc a
"""
text1 = aocd.get_data(day=day, year=year)


def run(program, reg):
    i = 0
    while i < len(program):
        line = program[i]

        # print(i, line)

        inst = line[0]

        if inst == 'hlf':
            reg[line[1]] >>= 1  # div by 2
        elif inst == 'tpl':
            reg[line[1]] *= 3
        elif inst == 'inc':
            reg[line[1]] += 1
        elif inst == 'jmp':
            # print('jmp', line[1])
            i += int(line[1])
            continue
        elif inst == 'jie':
            if reg[line[1]] % 2 == 0:
                i += int(line[2])
                continue
        elif inst == 'jio':
            if reg[line[1]] == 1:
                i += int(line[2])
                continue

        i += 1

    return reg


if __name__ == '__main__':
    pone = ''
    ptwo = ''


    text = text1
    text = text.strip().splitlines()
    program = [line.replace(',', '').replace('+', '').split() for line in text]

    reg = run(program, {'a': 0, 'b': 0})

    pone = reg['b']
    print(f"AOC {year} day {day}  Part One: {pone}")

    reg = run(program, {'a': 1, 'b': 0})
    ptwo = reg['b']

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
