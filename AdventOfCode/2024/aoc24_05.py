# Advent of Code
year = 2024
day = 5

import numpy as np
import aocd
import os
from pprint import pprint
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
text1 = aocd.get_data(day=day, year=year)

def check(update, rules):
    for p, page in enumerate(update):
        if page in rules:
            for earlier_page in update[:p]:
                if earlier_page in rules[page]:
                    return False, p
    return True, None

def reorder(update, rules):
    _update = update.copy()
    p = len(update)
    while p < len(update):
        page = update[p]
        if page in rules:
            for earlier_page in _update[:p]:
                if earlier_page in rules[page]:
                    _page = _update.pop(_update.index(earlier_page))
                    _update = _update[:p] + [_page] + _update[p:]
                    p -= 1
        p += 1
    return _update

if __name__ == '__main__':
    pone = 0
    ptwo = 0

    text = text1
    text = text.strip().splitlines()

    rules = dict()
    updates = list()

    for line in text:
        if '|' in line:
            a, b = (int(x) for x in line.split('|'))
            if a not in rules:
                rules[a] = [b]
            else:
                rules[a].append(b)
            continue

        if ',' in line:
            updates.append([int(x) for x in line.split(',')])

    for i in range(len(updates)-1, -1, -1):
        update = updates[i]
        flag, p = check(update, rules)
        if flag:
            pone += update[len(update) // 2]
            updates.pop(i)
        else:
            # print(0, update)
            while not flag:
                page = update.pop(p)
                index = min(update.index(i) for i in rules[page] if i in update)

                update.insert(index, page)

                # print(1, update)
                flag, p = check(update, rules)

            # print('F', update)
            ptwo += update[len(update) // 2]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
