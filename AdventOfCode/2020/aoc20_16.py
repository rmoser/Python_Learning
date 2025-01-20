# Advent of Code
year = 2020
day = 16

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import math

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""
text1 = aocd.get_data(day=day, year=year)


def check1(ticket, rules):
    result = []
    for num in ticket:
        if not any(lo <= num <= hi for rng in rules.values() for lo, hi in rng):
            result.append(num)
    return result

def label(tickets, rules):
    result = [''] * len(rules)
    possible_names = dict()
    for rule in rules:
        possible_names[rule] = []
        rng = rules[rule]
        for c, col in enumerate(tickets.T):
            if np.bitwise_or(np.bitwise_and(col >= rng[0][0], col <= rng[0][1]), np.bitwise_and(col >= rng[1][0], col <= rng[1][1])).all():
                possible_names[rule].append(c)

    while not all(result):
        for rule in possible_names:
            possible_cols = possible_names[rule]
            if len(possible_cols) == 1:
                c = possible_cols[0]
                result[c] = rule
                del rules[rule]
                for r in possible_names:
                    if c in possible_names[r]:
                        possible_names[r].remove(c)
                break

    return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    r, m, o = text.split('\n\n')

    rules = dict(line.split(': ') for line in r.splitlines())
    for rule in rules:
        rules[rule] = tuple((int(x), int(y)) for x, y in (rng.split('-') for rng in rules[rule].split(' or ')))

    tickets = [[int(x) for x in line.split(',')] for line in o.splitlines() if ',' in line]
    my_ticket = [int(x) for line in m.splitlines() for x in line.split(',') if ',' in line]

    pone = 0
    valid_tickets = [my_ticket]
    for ticket in tickets:
        res = check1(ticket, rules)
        if res:
            pone += sum(res)
        else:
            valid_tickets.append(ticket)

    tickets = np.array(valid_tickets, dtype=int)

    labels = label(tickets, rules)

    t = dict(zip(labels, my_ticket))

    ptwo = math.prod([my_ticket[i] if n.startswith('departure') else 1 for i, n in enumerate(labels)])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
