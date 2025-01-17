# Advent of Code
year = 2020
day = 8

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""
text1 = aocd.get_data(day=day, year=year)

def run(program):
    trace = []
    i = 0
    result = 0
    while True:
        if i in trace:
            return result, False, trace
        trace.append(i)
        if i >= len(program) or i < 0:
            break
        instruction, value = program[i]
        # print(i, instruction, value, result, trace)
        match instruction:
            case 'nop':
                i += 1

            case 'acc':
                result += value
                i += 1

            case 'jmp':
                i += value

    return result, True, trace

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    program = []
    for x in text:
        instr, num = x.split()
        program.append((instr, int(num)))

    pone, _, trace = run(program)

    for i in [x for x in trace if program[x][0] == 'nop']:
        prog = [list(x) for x in program]
        prog[i][0] = 'jmp'
        r, b, t = run(prog)
        if b:
            ptwo = r

    if not ptwo:
        for i in [x for x in trace if program[x][0] == 'jmp']:
            prog = [list(x) for x in program]
            prog[i][0] = 'nop'
            r, b, t = run(prog)
            if b:
                ptwo = r

    # print(max(t for t in trace if program[t][0] == 'jmp'))
    # for t in trace:
    #     if program[t][0] == 'nop' and t + program[t][1] >= len(program):
    #         print(t, program[t])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
