# Advent of Code
from itertools import groupby

year = 2023
day = 12

import numpy as np
import aocd
import itertools as it
import logging, sys
import functools
import math

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


text0 = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
#
# text0 = """
# .##.?#??.#.?# 2,1,1,1
# """
text1 = aocd.get_data(day=day, year=year)


@functools.cache
def brute(record, score):
    # if sum(score) + len(score) - 1 == len(record):
    #     return 1

    result = 0
    if '.' in record:
        records = [i for i in record.split('.') if i]
        n_records = len(records)
        n_scores = len(score)
        for n in range(n_scores):
            for i, group in enumerate(it.combinations_with_replacement(range(n_records), n_scores)):
                print(records, list(group))
                s = []
                for j, id in enumerate(group):
                    s.append(list())
                    s[j].append(score[id] for )


    return


    # total = 1
    count = 0
    unknown = record.count('?')
    broken = sum(score) - record.count('#')
    unbroken = unknown - broken
    # for group in it.permutations('#.', r=unknown):
    logging.debug(f"Group:  {unknown}, {broken}, {unbroken}")
    for group in it.product("#.", repeat=unknown):
        l = list(group)
        if not l.count('#') == broken:
            continue
        s = ''.join((c if c in '#.' else l.pop(0) for c in record))
        logging.debug(f"{record}, {score}, {group}, {s}")
        i = is_match(s, score)
        if i:
            # logging.debug(f"{record}, {score}, {group}, {s}")
            pass
        count += i

    return count


@functools.cache
def is_match(record, score):
    s = tuple(len(x) for x in record.split('.') if x)
    return s == score


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()
    text = text[1:2]

    scores_1 = []
    scores_2 = []

    for line in text:
        # print(f"\n>>  {line}")
        record, score = line.split()
        # record = record.strip('.')
        score = tuple((int(i) for i in score.split(',')))
        # logging.debug(f"{record} {score}")

        # while len(record) and record[0] == '#':
        #     i = score.pop(0)
        #     record = record[i+1:]
        #     record = record.strip('.')
        #
        # while len(record) and record[-1] == '#':
        #     i = score.pop(-1)
        #     record = record[:-i]
        #     record = record.strip('.')


        scores_1.append(brute(record, score))
        break
        record_2 = f"{record}?"*5
        scores_2.append(brute(record_2, score*5))

    pone = sum(scores_1)
    ptwo = sum(scores_2)
    # print(record, score, record_count)


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
