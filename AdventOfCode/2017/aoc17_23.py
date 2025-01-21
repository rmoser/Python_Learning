# Advent of Code
year = 2017
day = 23

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import pandas as pd

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"


text0 = """
"""
text1 = aocd.get_data(day=day, year=year)

DEBUG = 2

def run(prog, a=0, end=None):
    reg = dict()
    for x in 'bcdefgh':
        reg[x] = 0
    reg['a'] = a

    def my_eval(i):
        if i in reg:
            return reg[i]
        return int(i)

    i = 0
    mul_count = 0
    op_count = 0

    if bool(end):
        df = pd.DataFrame(np.zeros((end, 9), dtype=int), columns=list('iabcdefgh'))
        df['i'] = ' '*20
        df.loc[0] = ['', a,0,0,0,0,0,0,0]
    else:
        df = None

    while i < len(prog):
        inst, arg, val = prog[i]

        _arg = my_eval(arg)
        _val = my_eval(val)

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

        if df is not None:
            df.loc[op_count] = [' '.join(prog[i])] + list(reg[x] for x in 'abcdefgh')

            if op_count == end:
                # df.to_csv(r'G:\temp\out.csv')
                break

        i += inc

        # if DEBUG == 2 or DEBUG == 1 and (op_count & 1023 == 0):
        #     print(f"{op_count} {mul_count}\t\t{i}:{inst}  {arg}: {_arg}, {val}: {_val}, {reg}")


    return mul_count, reg['h'], df

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    prog = [line.split() for line in text]

    pone, _, _ = run(prog)
    print(f"AOC {year} day {day}  Part One: {pone}")

    _, ptwo, df = run(prog, 1, end=10000)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
