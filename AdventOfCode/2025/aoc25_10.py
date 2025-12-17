# Advent of Code
year = 2025
day = 10

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic
import itertools as it
import sympy as sy
import math
from pathos.pools import ProcessPool

MP = False

# Disable system sleep mode while this script runs
import ctypes
ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)

text0 = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
text1 = aocd.get_data(day=day, year=year)

def solve(goal, buttons, joltage):
    for i in range(1, len(buttons)+1):
        for group in it.combinations(buttons, i):
            # ic(group)
            state = np.zeros_like(goal, dtype=bool)
            for button in group:
                state ^= button
            if (state == goal).all():
                return len(group), group
    return 0

def get_max(button, joltage):
    if not isinstance(joltage, np.ndarray):
        joltage = np.array(joltage)
    vals = np.where(button)
    return joltage[vals].min()


def reduce(buttons, joltage):
    ans = np.zeros((buttons.shape[0], 1), dtype=np.uint)

    # Find joltage values where only one button contributes
    uniques = np.where(buttons.sum(axis=0)==1)[0]
    while len(uniques) > sum(ans>0):
        for i in uniques:
            b = np.where(buttons[:, i])[0].min()
            ans[b] = joltage[i]
            ic(f"Uniques: Press button {b} {ans[b]} times...")
            # buttons[b].mask = True
        uniques = np.where(buttons.sum(axis=0)==1)[0]

    return ans, buttons


def solve2(_, buttons, joltage):
    ans_set = _solve2(_, buttons, joltage)
    return optimize(ans_set)


def _solve2(_, buttons, joltage):
    b = buttons.T.astype(int)
    j = np.expand_dims(np.array(joltage),1)
    m = np.concatenate((b,j),axis=1)

    M = sy.Matrix(m.tolist())

    system = A, b = M[:, :-1], M[:, -1]
    return sy.linsolve(system)

def free_symbol_names(ans_set):
    return tuple((str(x) for x in ans_set.free_symbols))

def periodicity(ans_set):
    free_symbols = free_symbol_names(ans_set)
    n_free_symbols = len(free_symbols)
    ans_set_str = str(ans_set.args[0])[1:-1].split(', ')
    try:
        step = min((int(z[1]) for z in [x.split(r'/') for term in ans_set_str for x in term.split(' ') if len(x)>1] if len(z) > 1))
    except (IndexError, ValueError):
        step = 1
    offset = (0,) * n_free_symbols
    if step > 1:
        for i in it.product(range(step), repeat=n_free_symbols):
            a = ans_set.subs(dict(zip(free_symbols, i))).args[0]
            if all(int(x) == x for x in a):
                offset = i
                break

    return step, offset

def min_max(ans_set) -> dict:
    ranges = dict()
    for s in ans_set.free_symbols:
        ranges[s] = [0, 1000, 1]

        for arg in ans_set.args[0]:
            if len(arg.free_symbols) == 1 and s in arg.free_symbols:
                i = sy.solve(arg, s)[0]
                ic(arg, s, '=> ', i)
                i1 = arg.subs(s, i+1)
                if i1 > 0 and i > ranges[s][0]:
                        # New lower bound
                        ic("Old:", ranges[s])
                        # ranges[s][0] = max(ranges[s][0], math.ceil(i.evalf()))
                        ranges[s][0] = i
                        ic("New:", ranges[s])
                elif i1 < 0 and i < ranges[s][1]:
                        # New upper bound
                        ic("Old:", ranges[s])
                        ranges[s][1] = i
                        ic("New:", ranges[s])

    p = periodicity(ans_set)
    for i, s in enumerate(ans_set.free_symbols):
        v = p[1][i]
        if ranges[s][0] == 0:
            ranges[s][0] = v

    return ranges


def all_ints(arr):
    return (arr % 1 == 0).all()


def _optimize(ans_set):
    free_symbols = free_symbol_names(ans_set)
    n_free_symbols = len(free_symbols)

    results = dict()
    if n_free_symbols == 0:
        arr = np.array(ans_set.args[0])
        if all_ints(arr) and (arr >= 0).all():
            results[ans_set.args[0]] = sum(ans_set.args[0])
        return results

    ranges = min_max(ans_set)
    size = np.inf
    free_symbol = ''
    r = None
    for k, v in ranges.items():
        s = 1+v[1]-v[0]
        if s < size:
            size = s
            free_symbol = k
            r = v
    if free_symbol:
        if r[0] % r[2] == 0:
            r = np.arange(r[0], r[1] + 1, r[2])
        else:
            r = np.arange(r[0] - r[0]%r[2], r[1]+1, r[2])

    # size = 1 + max(x[1] for x in ranges.values())
    # if isinstance(size, sy.core.numbers.Number):
    #     size = math.ceil(size.evalf())

    ic(ans_set, size, free_symbol)

    ic(f'_optimize1-ing: {free_symbol} of {free_symbols}: {size}')
    for i in r:
        a = ans_set.subs(dict({free_symbol: i}))
        print(a)
        results.update(_optimize(a))

    return results

def optimize(ans_set):
    results = _optimize(ans_set)
    result = None
    size = np.inf
    for k, v in results.items():
        if v < size:
            result, size = k, v

    return result

def check(ans_set, machine):
    _, buttons, joltage = machine
    if not (buttons.T.dot(ans_set) == joltage).all():
        return False
    a = np.array(ans_set)
    if not (a >= 0).all():
        return False
    if not ((a % 1) == 0).all():
        return False
    return True

def score(ans_set, args):
    free_symbols = free_symbol_names(ans_set)
    vals = ans_set.subs(dict(zip(free_symbols, args))).args[0]

    neg = 100 * sum((x if x<0 else 0 for x in vals)) ** 2
    ints = 100 * sum((x if int(x) != x else 0 for x in vals)) ** 2
    dist = sum((x**2 for x in vals))
    return float(dist + neg + ints)


def run(x):
    a = solve2(*m)
    ic.enable()
    ic(z, a, check(a, m))
    ic.disable()
    return a


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    machines = []
    for line in text:
        words = line.split()
        goal = np.array([0 if x == '.' else 1 for x in words[0][1:-1]], dtype=bool)
        buttons = [[int(y) for y in x[1:-1].split(',')] for x in words[1:-1]]
        buttons = np.array([[i in button for i in range(len(goal))] for button in buttons])

        joltage = [int(x) for x in words[-1][1:-1].split(',')]
        # ic(goal, buttons, joltage)
        machines.append([goal, buttons, joltage])

    # ic(solve(*machines[0]))
    pone = sum((solve(*machine)[0] for machine in machines))

    print(f"AOC {year} day {day}  Part One: {pone}")

    results = np.zeros(len(machines), dtype=int)
    if True:
        if MP:
            pool = ProcessPool()
            results = pool.imap(run, machines)

        else:
            # ic.enable()
            ic.disable()
            for z, m in enumerate(machines):
                # a = _solve2(*m)
                # s = optimize1(a)
                a = run(m)
                results[z] = sum(a)
                # results[z] = sum(s)

        ptwo = sum(results)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
