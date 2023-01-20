# Advent of Code
year = 2021
day = 24

import numpy as np
import aocd
import itertools

text0 = """
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""
text1 = aocd.get_data(day=day, year=year)


def alu(program, number):
    number = [int(c) for c in list(number)]
    # print(number)

    data = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for line in program:
        inst = line.split()
        # print(inst)

        a = inst[1]

        b = None
        if len(inst) > 2:
            b = inst[2]
            if b in 'wxyz':
                b = data[b]
            else:
                b = int(b)

        # print(inst[0], inst[1:], '->', b)

        if inst[0] == 'inp':
            data[a] = number.pop(0)
            # print(f"INP {a} = {data[a]}")
            continue

        if inst[0] == 'add':
            # print(f"{a}+{b}: {data[a]} + {data[b] if b in data else b}")
            data[a] = data[a] + b
            # print(f"{a} + {b} = {data[a]}")
            continue

        if inst[0] == 'mul':
            # print(f"{a}*{b}: {data[a]} * {data[b] if b in data else b}")
            data[a] = data[a] * b
            # print(f"{a} * {b} = {data[a]}")
            continue

        if inst[0] == 'div':
            # print(f"{a}/{b}: {data[a]} / {data[b] if b in data else b}")
            data[a] = data[a] // b
            # print(f"{a} / {b} = {data[a]}")
            continue

        if inst[0] == 'mod':
            # print(f"{a}%{b}: {data[a]} % {data[b] if b in data else b}")
            data[a] = data[a] % b
            # print(f"{a} % {b} = {data[a]}")
            continue

        if inst[0] == 'eql':
            # print(f"{a}=={b}: {data[a]} == {data[b] if b in data else b}")
            data[a] = int(data[a] == b)
            # print(f"{a} == {b}: {data[a]}")
            continue

    # print(data)

    return data


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    for model in itertools.combinations_with_replacement('987654321', 14):
        data = alu(text, ''.join(model))
        print(model, data['z'])
        if data['z'] == 0:
            pone = ''.join(model)
            break

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
