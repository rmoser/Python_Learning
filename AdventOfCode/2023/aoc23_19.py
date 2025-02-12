# Advent of Code
year = 2023
day = 19

import numpy as np
import aocd
import os
import utils
from pprint import pprint
import itertools as it
import math
import collections
from copy import deepcopy

text0 = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
#
# text0 = """
# in{s<2001:sd,A}
# sd{x<2001:R,A}
#
# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}
# """

text1 = aocd.get_data(day=day, year=year)

def parse(rule):
    result = []
    for r in rule.split(','):
        if ':' in r:
            comp, target = r.split(':')
            var = comp[0]
            op = comp[1]
            val = int(comp[2:])
            result.append((var, op, val, target))
        else:
            result.append(r)
    return result

def run(xmas, rules):
    rule = 'in'
    while True:
        for r in rules[rule]:
            if not isinstance(r, tuple):
                rule = r
                break

            var, op, val, target = r
            if op == '>' and xmas[var] > val:
                rule = target
                break
            if op == '<' and xmas[var] < val:
                rule = target
                break

        if rule in 'AR':
            return rule == 'A'

def run2(xmas, rule='in', rules=None):
    xmas = deepcopy(xmas)
    result = 0
    if rule in 'AR':
        if rule == 'A':
            vals = np.array(list(xmas.values()))
            result += np.prod(np.diff(vals))
        return result

    if rule not in rules:
        raise KeyError(f'Key not found: {rule}')

    for r in rules[rule]:
        if not isinstance(r, tuple):
            return result + run2(xmas, r, rules)

        var, op, val, target = r
        if op == '>':  # do for values > 2000
            if xmas[var][1] <= val:  # skip if max <= 2000
                continue

            a = deepcopy(xmas)
            a[var][0] = max(a[var][0], val+1)  # a_min = max(a_min, 2001)
            rule = target
            # Recurse on the range that matches the rule
            result += run2(a, rule=rule, rules=rules)
            # Reduce the remaining range for further rule checks
            xmas[var][1] = min(xmas[var][1], val+1)  # x_max - min(x_max, 2001)

        if op == '<':  # do for values < 2000
            if xmas[var][0] > val:  # min > 2000
                continue

            a = deepcopy(xmas)
            a[var][1] = min(a[var][1], val)  # matched: max is min(4000, 2000)
            rule = target
            result += run2(a, rule=rule, rules=rules)
            xmas[var][0] = max(xmas[var][0], val)  # not matched:  min = max(max, 2000)



if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n' if '\n\n' in text else '\n')

    rules = dict()
    for line in text[0].split('\n'):
        label, rules_text = line[:-1].split('{')
        rules[label] = parse(rules_text)

    pone = 0
    for line in text[1].split('\n'):
        xmas = dict(zip('xmas', [int(i[2:]) for i in line.strip('{}').split(',')]))
        if run(xmas, rules):
            pone += sum(xmas.values())

    print(f"AOC {year} day {day}  Part One: {pone}")

    XMAS = {'x': [1, 4001], 'm': [1, 4001], 'a': [1, 4001], 's': [1, 4001]}

    ptwo = run2(XMAS.copy(), 'in', rules)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
