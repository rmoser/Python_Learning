# Advent of Code
year = 2020
day = 14

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

text0 = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""
text1 = aocd.get_data(day=day, year=year)

def parse_mask(text):
    mask = {'0': [], '1': [], 'X': []}
    for i, c in enumerate(text[::-1]):
        mask[c].append(i)
    return mask

def expand_mask(text):
    stack = [text]
    result = []
    while stack:
        s = stack.pop(0)
        if 'X' not in s:
            result.append(s)
            continue

        i = s.index('X')
        for c in '01':
            stack.append(s[:i] + c + s[i+1:])
    return result

def run_one(text):
    memory = dict()
    for line in text:
        op, value = line.split(' = ')
        if op == 'mask':
            mask = parse_mask(value)
            continue

        addr = int(op[4:-1])
        value = list(format(int(value), '036b'))
        for i in mask['0']:
            value[-i-1] = '0'
        for i in mask['1']:
            value[-i-1] = '1'
        memory[addr] = int(''.join(value), 2)
    return memory


def run_two(text):
    memory = dict()
    for line in text:
        op, value = line.split(' = ')
        if op == 'mask':
            mask = parse_mask(value)
            # print(value, len(mask['X']))
            continue

        addr = list(format(int(op[4:-1]), '036b'))
        value = int(value)
        for i in mask['1']:
            addr[-i-1] = '1'
        for i in mask['X']:
            addr[-i-1] = 'X'
        addr = ''.join(addr)
        addr = tuple(sorted(list(expand_mask(addr))))
        for a, v in list(memory.items()):
            # Update memory for overwritten addresses
            if any(x in a for x in addr):
                del memory[a]
                memory[tuple(x for x in a if x not in addr)] = v
        memory[addr] = value
        # pprint(memory)

    return memory


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    memory = run_one(text)

    pone = sum(memory.values())
    print(f"AOC {year} day {day}  Part One: {pone}")

    memory2 = run_two(text)
    ptwo = sum(len(k) * v for k, v in memory2.items())
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
