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
import tempfile

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"


text0 = """
set b 81
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23
"""
text1 = aocd.get_data(day=day, year=year)

DEBUG = 2

def run2(a, b=None, c=None):

    d = 0
    e = 0
    f = 0
    g = 0
    h = 0

    if b is None:
        b = 81
    if c is None:
        c = b
    if a:
        b *= 100
        b += 100000
        c = b + 17000

    while True:  # While b != c
        f = 1
        d = 2
        while True:  # While d != b
            e = 2
            d += 1
            g -= 1



def run(prog, a=0, end=None):
    reg = dict()
    for x in 'abcdefgh':
        reg[x] = 0
    reg['a'] = a

    threshold = 100


    def my_eval(i):
        if i in reg:
            return reg[i]
        return int(i)

    i = 0
    mul_count = 0
    op_count = 0

    df = None
    log = None
    log1 = None

    if bool(end):
        log = open(rf'g:\temp\out_{a}.csv', 'w')
        # log1 = open(r'g:\temp\h.csv', 'w')

        cols = 'op,i,inst,' + ','.join(list('abcdefgh'))
        row0 = '\n' + ','.join(str(x) for x in [0, 0, '', a,0,0,0,0,0,0,0])
        if log is not None:
            log.write(cols)
            log.write(row0)
        if log1 is not None:
            log1.write(cols)
            log1.write(row0)
        # df = pd.DataFrame(np.zeros((end, 9), dtype=int), columns=list('iabcdefgh'))
        # df['i'] = ' '*20
        # df.loc[0] = ['', a,0,0,0,0,0,0,0]

    while i < len(prog):
        inst, arg, val = prog[i]

        _arg = my_eval(arg)
        _val = my_eval(val)

        op_count += 1

        h = reg['h']

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

        h_changed = reg['h'] != h

        if end is not None:
            data = [op_count, i, ' '.join(prog[i])] + list(reg.values())
            line = '\n' + ','.join(str(x) for x in data)
            if log is not None:
                log.write(line)
            if log1 is not None and h_changed:
                log.write(line)

            # df.loc[op_count] = [' '.join(prog[i])] + list(reg[x] for x in 'abcdefgh')

            if op_count == end:
                if log is not None:
                    log.close()
                if log1 is not None:
                    log1.close()
                # df.to_csv(r'G:\temp\out.csv')
                break

        i += inc

        if op_count % threshold == 0:
            print(f"{op_count:>12}: {i}.{inst}  {arg}: {_arg}, {val}: {_val}, {reg}")
            if len(str(op_count)) > len(str(threshold)):
                threshold *= 10

    # if DEBUG == 2 or DEBUG == 1 and (op_count & 1023 == 0):
        #     print(f"{op_count} {mul_count}\t\t{i}:{inst}  {arg}: {_arg}, {val}: {_val}, {reg}")


    return mul_count, reg['h']

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    prog = [line.split() for line in text]

    pone, h = run(prog)
    print(f"AOC {year} day {day}  Part One: {pone}")

    # _, ptwo = run(prog, 1, end=10000000)
    ptwo = sum(not utils.is_prime(n) for n in range(108100, 125101, 17))
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
