# Advent of Code
year = 2020
day = 19

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import re

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

text0 = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""
text1 = aocd.get_data(day=day, year=year)

RULES = dict()
DONE = set()
MAXLEN = 0

DEBUG = False

def flatten(obj):
    return it.chain.from_iterable([o] if isinstance(o, str) else o for o in obj)

def to_re(obj):
    # Find self-reference
    for rule in flatten(obj):
        if not rule in DONE:
            break
    i = obj.index(rule)
    base = _parse(obj[:i]),  _parse(obj[i+1:])

    # new = base.copy()
    # while max(len(x) for x in new) < MAXLEN:
    #     new = [''.join(x) for x in it.product(base, new)]
    #
    # print(new)
    pat = (re.compile(f'^(?:{"|".join(_parse(obj[0]))})'), )
    if len(obj) > 2:
        pat = pat + (re.compile(f'(?:{"|".join(_parse(obj[-1]))})$'), )

    return pat


def _parse(obj):
    try:
        # string is either a key to dereference or a fixed value
        if isinstance(obj, re.Pattern):
            return obj

        if isinstance(obj, str):
            if not obj.isnumeric():
                return obj
            if obj in DONE:
                return RULES[obj]
            return ''

        if hasattr(obj, '__iter__'):
            if len(obj) == 0:
                return ''
            if len(obj) == 1:
                return _parse(obj[0])

        if DEBUG:
            print(f'parse: "{obj}"')

        # tuple is one or more items to concat
        if isinstance(obj, tuple):
            temp0 = tuple(_parse(x) for x in obj)
            if all(isinstance(x, re.Pattern) for x in flatten(temp0)):
                # return re.compile('^' + ''.join(pat.pattern[1:-1] for pat in temp0) + '$')
                return temp0
            temp1 = [''.join(x) for x in it.product(*temp0)]
            return temp1

        # list is options to choose from for each index
        if isinstance(obj, list):
            rule = ''
            for x in flatten(obj):
                if isinstance(x, str) and x.isnumeric() and x not in DONE:
                    # Self-reference
                    rule = x
                    break
            if rule:
                # print(f'Self-reference: \'{rule}\': {obj[1]}')
                return to_re(obj[1])

            obj = [_parse(x) for x in obj]
            # List of lists
            if isinstance(obj[0], list):
                obj = [x if isinstance(x, list) else [x] for x in obj]
                obj = [y for x in obj for y in x]

            return obj
    except TypeError:
        raise(TypeError(f'_parse({obj}'))

def parse():
    first = True
    # DONE.clear()
    while RULES.keys() != DONE:
        todo = set(RULES) - DONE
        if first:
            ready = [rule for rule in todo if isinstance(RULES[rule], str) and not RULES[rule].isnumeric()]
            first = False
        else:
            ready = [rule for rule in todo if all(i in DONE for i in flatten(RULES[rule]))]
            # ready = [rule for rule in todo if all(i in DONE for j in RULES[rule] for i in list(j))]
        if not ready:
            # Handle self-referential rules
            ready = [rule for rule in todo if rule in flatten(RULES[rule])]
        # print(f'Done: {len(DONE)}, Ready: {len(ready)}, Todo: {len(todo)}')
        for rule in ready:
            value = RULES[rule]
            # print(rule, value)
            x = _parse(value)
            if x:
                RULES[rule] = x
                DONE.add(rule)

            continue

def my_match(t, patterns):
    if len(patterns) == 1:
        p0 = patterns[0]
        while True:
            m0 = re.search(p0, t)
            if m0:
                s = m0.span()
                t = t[:s[0]] + t[s[1]:]
                if not t:
                    return True
                continue
            return False


    p0, p1 = patterns

    while True:
        m0 = re.search(p0, t)
        m1 = re.search(p1, t)
        if bool(m0) and bool(m1):
            s0 = m0.span()
            s1 = m1.span()
            t = t[:s0[0]] + t[s0[1]:s1[0]] + t[s1[1]:]
            if not t:
                return True
            continue
        return False


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    rules, messages = text.split('\n\n')

    messages = messages.splitlines()
    MAXLEN = max(len(m) for m in messages)

    RULES = dict(x.split(': ') for x in rules.splitlines())
    for rule, value in RULES.items():
        if '"' in value:
            RULES[rule] = value[1:-1]
            continue
        if '|' in value:
            RULES[rule] = list(tuple(x.split()) for x in value.split(' | '))
            continue
        RULES[rule] = tuple(value.split())

    rules = RULES.copy()

    parse()
    pone = len(set(messages) & set(RULES['0']))

    print(f"AOC {year} day {day}  Part One: {pone}")

    RULES['0'] = ('8', '11')
    RULES['8'] = [('42',), ('42', '8')]
    RULES['11'] = [('42', '31'), ('42', '11', '31')]
    DONE -= {'0', '8', '11'}

    parse()

    pat = RULES['0']
    ptwo = 0

    _step = max(len(x) for x in RULES['42'])

    for m in messages:
        # print(m)
        for i in range(_step, len(m), _step):
            a, b = m[:i], m[i:]
            m_a = my_match(a, pat[0])
            m_b = my_match(b, pat[1])
            # print(i, a, b, m_a, m_b)

            if m_a and m_b:
                ptwo += 1
                # print('Match')
                break

    # for m in messages:
    #     if re.match(pat, m):
    #         print(m)
    #         ptwo += 1

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
