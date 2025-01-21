# Advent of Code
year = 2017
day = 18

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import collections
import threading
import time

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
"""

text0 = """
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
"""
text1 = aocd.get_data(day=day, year=year)

QUEUE = (collections.deque(), collections.deque())
SENT = [0, 0]
RCV = [0, 0]
ITERS = [0, 0]
GLOBAL_EXIT = False
OPS = ['', '']


def run(prog, self=0, steps=None):
    i = 0
    s = 0
    other = 1-self
    registers = collections.defaultdict(int)

    def my_val(x):
        if x.isnumeric() or x[0] == '-' and x[1:].isnumeric():
            return int(x)
        return registers[x]

    while i < len(prog):
        s += 1
        if steps is not None and s > steps:
            break

        line = prog[i]
        op, reg = line[:2]
        val = line[2] if len(line) == 3 else 'NOP'

        # print(i, line, registers)


        match op:
            case 'snd':
                QUEUE[other].append(my_val(reg))

            case 'set':
                registers[reg] = my_val(val)
            case 'add':
                registers[reg] += my_val(val)
            case 'mul':
                registers[reg] *= my_val(val)
            case 'mod':
                registers[reg] %= my_val(val)
            case 'rcv':
                if my_val(reg) != 0:
                    return QUEUE[other].pop()
            case 'jgz':
                # print(f'{reg}: {eval(reg)}, {val}: {eval(val)}')
                if my_val(reg) > 0:
                    i += my_val(val)
                    continue
        i += 1


def run2(prog, self=0, steps=None):
    i = 0
    s = 0
    other = 1-self
    registers = collections.defaultdict(int)
    registers['p'] = self
    global GLOBAL_EXIT, QUEUE, SENT, RCV, ITERS, OPS

    def my_val(x):
        if x.isnumeric() or x[0] == '-' and x[1:].isnumeric():
            return int(x)
        return registers[x]

    while i < len(prog):
        if GLOBAL_EXIT:
            return

        ITERS[self] += 1
        s += 1
        if steps is not None and s > steps:
            break

        line = prog[i]
        op, reg = line[:2]
        OPS[self] = op
        if len(line) == 3:
            val = line[2]
        else:
            val = 'NOP'

        # print(f'\nQ({len(QUEUE[0])}, {len(QUEUE[1])}) == Op: {OPS}, Sent: {SENT}, Rcv: {RCV}, Iters: {ITERS}')
        # print(f'{self}: i:{i}, line: {line}, reg: {registers}')

        match op:
            case 'snd':
                QUEUE[other].append(my_val(reg))
                SENT[self] += 1
            case 'set':
                registers[reg] = my_val(val)
            case 'add':
                registers[reg] += my_val(val)
            case 'mul':
                registers[reg] *= my_val(val)
            case 'mod':
                registers[reg] %= my_val(val)
            case 'rcv':
                while len(QUEUE[self]) == 0:
                    if OPS[other] == 'rcv' and len(QUEUE[other]) == 0:
                        GLOBAL_EXIT = True
                        return
                    time.sleep(0)

                registers[reg] = QUEUE[self].popleft()
                RCV[self] += 1

            case 'jgz':
                # print(f'{reg}: {eval(reg)}, {val}: {eval(val)}')
                if my_val(reg) > 0:
                    i += my_val(val)
                    continue
        i += 1


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    prog = [line.split() for line in text]

    pone = run(prog, 0)

    print(f"AOC {year} day {day}  Part One: {pone}")

    QUEUE[0].clear()
    QUEUE[1].clear()
    t0 = threading.Thread(target=run2, args=(prog, 0))
    t1 = threading.Thread(target=run2, args=(prog, 1))

    t0.start()
    t1.start()


    t0.join()
    t1.join()


    # GLOBAL_EXIT = True

    ptwo = SENT[1]

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
