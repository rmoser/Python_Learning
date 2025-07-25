# Advent of Code
year = 2020
day = 7

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import re
import functools

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

text0 = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

text1 = aocd.get_data(day=day, year=year)

BAGS = dict()

@functools.cache
def contains_color(bag, color='shiny gold'):
    if color in BAGS[bag]:
        return True
    return any(contains_color(b, color) for b in BAGS[bag].keys())

@functools.cache
def count_bag(bag):
    if not BAGS[bag]:
        return 0
    return sum(v * (1+count_bag(k)) for k, v in BAGS[bag].items())

def parse(line):
    a, b = line[:-1].split(' contain ')
    # print(a, ':', b)
    color = ' '.join(a.split()[:2])
    bag = dict()
    BAGS[color] = bag
    for content in b.split(', '):
        content = content.split()
        # print(content)
        if content[0].isnumeric():
            n = int(content[0])
            content_color = ' '.join(content[1:3])
            bag[content_color] = n

    # # print('\n', line)
    # # match = re.match(r'^([\w\s]+) bags contain', line)
    # match = re.match(r'(\w+\s\w+) bags contain (\d+)? ?(\w+\s\w+) bags?(?:, (\d+) (\w+\s\w+) bags?)+.', line)
    # if match:
    #     print(match.groups())
    #     color, a, color_a,  b, color_b = match.groups()
    #     new_dict = dict()
    #     if a:
    #         new_dict[color_a] = a
    #     if b:
    #         new_dict[color_b] = b

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    for line in text:
        parse(line)

    pone = sum(contains_color(b) for b in BAGS.keys())
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = count_bag('shiny gold')
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
