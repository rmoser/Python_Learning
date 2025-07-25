# Advent of Code
import collections

year = 2017
day = 25

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
    """
text1 = aocd.get_data(day=day, year=year)

def parse(text):
    logic = dict()

    header = text[0].splitlines()
    start = header[0].split()[-1][:-1]
    loops = int(header[1].split()[-2])

    logic['start'] = start
    logic['loops'] = loops

    def _parse(rules):
        obj = dict()
        name = rules[0].split()[-1][:-1]
        obj['name'] = name

        for r in (1, 5):
            i = 0 if '0' in rules[r] else 1
            v = 0 if '0' in rules[r+1] else 1
            direction = 'r' if 'right' in rules[r+2] else 'l'
            state = rules[r+3].split()[-1][:-1]
            obj[i] = (v, direction, state)

        return obj

    for rule in text[1:]:
        x = _parse(rule.splitlines())
        logic[x['name']] = x

    return logic

def run(logic):
    data = collections.defaultdict(int)
    i = 0
    state = logic['start']

    for _ in range(logic['loops']):
        write_val, move, next_state = logic[state][data[i]]
        data[i] = write_val
        i += 1 if move == 'r' else -1
        state = next_state

    return data


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n')

    logic = parse(text)

    data = run(logic)
    pone = sum(data.values())
    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
