# Advent of Code
year = 2023
day = 5

import numpy as np
import aocd
import os
import utils
from pprint import pprint
import itertools as it
import math

text0 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
text1 = aocd.get_data(day=day, year=year)

def parse(text):
    rules = dict()
    for section in text:
        for line in section.splitlines():
            if line.startswith('seeds:'):
                rules['seed'] = [int(x) for x in line[7:].split()]
                continue

            if line.endswith(' map:'):
                rule = line.replace(' map:', '').split('-')
                rule = rule[0], rule[-1]
                continue

            rules[rule] = rules.get(rule, list()) + [tuple(int(x) for x in line.split())]
    return rules

def valid(ranges):
    for a, b in it.combinations(ranges, 2):
        if b[0] <= sum(a) < sum(b):
            return False
        if a[0] <= sum(b) < sum(a):
            return False
    return True

def compress(ranges):
    result = []

    _ranges = sorted(ranges)

    a = _ranges[0]
    for b in _ranges[1:]:
        # a and b are consecutive
        if a[0] + a[1] == b[0]:
            a = a[0], a[1] + b[1]
            continue

        # a == b
        if a == b:
            continue

        # b overlaps a:
        if a[0] <= b[0] < a[1]:
            a = a[0], max(sum(a), sum(b))
            continue

        result.append(a)
        a = b
    result.append(a)

    return result


def map_all(seeds, rules):
    next_rule = 'seed'

    while True:
        match_rule = tuple(x for x in rules if x[0] == next_rule)
        if not match_rule:
            break
        rule = match_rule[0]
        next_rule = rule[1]
        seeds = map_range(seeds, rules[rule])

    return seeds


def map_range(src_ranges, dest_maps):
    # inputs = (79 14), (55 13)
    # ranges = [(0, 15, 37), (52, 50, 48)]

    # (79, 14) -> (0, 15, 37)   => No overlap
    # (79, 14) -> (52, 50, 48)  => (81, 14)

    # (55, 13) -> (0, 15, 37):  => No overlap
    # (55, 13) -> (52, 50, 48): => (57, 13)

    result = []
    for src_range in src_ranges:
        for dest_map in dest_maps:
            map_in = dest_map[1], dest_map[2]
            map_out = dest_map[0], dest_map[2]
            offset = dest_map[0] - dest_map[1]

            # No overlap
            if src_range[0] >= sum(map_in) or sum(src_range) <= map_in[0]:
                continue

            # src_range included in dest_rng:
            if map_in[0] <= src_range[0] and sum(src_range) <= sum(map_in):
                result.append((src_range[0] + offset, src_range[1]))
                src_range = (src_range[0], 0)
                continue

            # Only start of src_range overlaps map_in:
            if map_in[0] <= src_range[0] and sum(src_range) > sum(map_in):
                overlap = sum(map_in) - src_range[0]
                result.append((src_range[0]+offset, overlap))
                src_range = sum(map_in), src_range[1]-overlap
                continue

            # Only end of src_range overlaps map_in
            if map_in[0] > src_range[0] and sum(src_range) <= sum(map_in):
                overlap = sum(src_range) - map_in[0]
                result.append((map_out[0], overlap))
                src_range = src_range[0], src_range[1]-overlap
                continue

        # Any unmapped ranges propagate to the next map
        if src_range[1]:
            result.append(src_range)
    return result

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n' if '\n\n' in text else '\n')

    rules = parse(text)

    seeds = [(x, 1) for x in rules['seed']]

    pone_seeds = map_all(seeds, rules)
    pone = min(pone_seeds)[0]
    print(f"AOC {year} day {day}  Part One: {pone}")

    seeds = list(zip(rules['seed'][0::2], rules['seed'][1::2]))
    ptwo_seeds = map_all(seeds, rules)

    ptwo = min(ptwo_seeds)[0]
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
