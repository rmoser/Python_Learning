# Advent of Code
year = 2021
day = 14

import numpy as np
import aocd
import math

text0 = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
text1 = aocd.get_data(day=day, year=year)

def parse_pair(pairs, d, n=1):
    for _ in range(n):
        new = dict()
        for pair, count in pairs.items():
            a, b = pair
            c = d[pair]
            new[(a, c)] = new.get((a, c), 0) + count
            new[(c, b)] = new.get((c, b), 0) + count
        pairs.clear()
        for pair in new:
             pairs[pair] = new[pair]

    return pairs


def count_chars(pairs):
    result = dict()
    for (a, b), n in pairs.items():
        result[a] = result.get(a, 0) + n
        result[b] = result.get(b, 0) + n
    return result


def check_string(s, pairs):
    check = dict()
    result = True
    for pair in zip(s[:-1], s[1:]):
        check[pair] = check.get(pair, 0) + 1

    for pair in set(list(pairs.keys()) + list(check.keys())):
        if pairs[pair] != check[pair]:
            result = False
            print(f"Mismatch {pair}: {pairs[pair]} -> {check[pair]}")

    return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    s = text[0]
    pairs = dict()
    for pair in zip(s[:-1], s[1:]):
        pairs[pair] = pairs.get(pair, 0) + 1

    d = dict()
    for x in text:
        if '->' in x:
            ab, c = x.split(' -> ')
            d[tuple(ab)] = c

    # print(s)
    # print(d)

    print(pairs)

    parse_pair(pairs, d, 10)
    rone = count_chars(pairs)
    pone = math.ceil(max(rone.values())/2) - math.ceil(min(rone.values())/2)

    stwo = parse_pair(pairs, d, 30)
    rtwo = count_chars(pairs)
    ptwo = math.ceil(max(rtwo.values())/2) - math.ceil(min(rtwo.values())/2)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
