# Advent of Code
year = 2024
day = 17

import numpy as np
import aocd
import os
import pandas as pd
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"


text0 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
text1 = aocd.get_data(day=day, year=year)

def run(prog, a, b, c):
    def combo(x):
        if x <= 3:
            return x
        if x == 4:
            return a
        if x == 5:
            return b
        if x == 6:
            return c
        return None

    i = 0
    out = []
    while i < len(prog):
        inst = prog[i]
        arg = prog[i+1]

        match inst:
            case 0:  # adv instruction
                a //= 2 ** combo(arg)

            case 1:  # bxl operator
                b ^= arg

            case 2:  # bst operator
                b = combo(arg) % 8

            case 3:  # jnz operator
                if a > 0:
                    i = arg
                    continue

            case 4:  # bxc operator
                b = b ^ c

            case 5:  # out operator
                out.append(combo(arg) % 8)

            case 6:  # bdv operator
                b = a // 2 ** combo(arg)

            case 7:  # cdv operator
                c = a // 2 ** combo(arg)

        i += 2

    return out


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    # print(text)
    for line in text:
        if not line:
            continue
        inst, val = line.split(': ')
        if inst == 'Register A':
            a = int(val)
        elif inst == 'Register B':
            b = int(val)
        elif inst == 'Register C':
            c = int(val)
        elif inst == 'Program':
            prog = [int(x) for x in val.split(',')]


    # print(a, b, c)
    # print(prog)

    out = run(prog, a, b, c)

    pone = ','.join((str(x) for x in out))

    p = np.array(prog)
    s = 0
    for i in range(len(prog)):
        s *= 8
        for j in range(1000):
            out = run(prog, s + j, b, c)
            # print('iter', s, f'a={s+j}', len(out), out, prog[-i-1:])
            if (out == p[-i-1:]).all():
                s += j
                # print(s, out, prog[-i-1:])
                break

    ptwo = s

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
