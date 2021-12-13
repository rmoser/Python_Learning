# Advent of Code
import itertools

year = 2015
day = 13

import numpy as np
import aocd

import itertools

text0 = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""
text1 = aocd.get_data(day=day, year=year)

happy = {}
names = {}


def score_plan(plan):
    score = 0
    n = len(plan)
    # print('\n', plan, n)
    for i, c in enumerate(plan):
        other = plan[(i-1) % n]
        _score = happy[f"{c}.{other}"]
        # print(f"{i} {c}.{other}", _score)
        score += _score

        other = plan[(i+1) % n]
        _score = happy[f"{c}.{other}"]
        # print(f"{i} {c}.{other}", _score)
        score += _score
    return score


if __name__ == '__main__':
    text = text1
    text = [x.split() for x in text.strip().splitlines()]

    for line in text:
        a = line[0]
        b = line[-1][:-1]
        score = int(line[3])
        score *= 1 if line[2] == 'gain' else -1

        happy[f'{a}.{b}'] = score

        names[a] = 1
        names[b] = 1

    names = list(names.keys())

    # print(happy)
    # print(names)

    scores = []
    first = [names[0]]
    for _plan in itertools.permutations(names[1:]):
        plan = first + list(_plan)
        score = score_plan(plan)
        # print(plan, score)
        scores.append(score)

    pone = max(scores)

    for name in names:
        happy[f'Me.{name}'] = 0
        happy[f'{name}.Me'] = 0

    names.append('Me')

    scores = []
    first = [names[0]]
    for _plan in itertools.permutations(names[1:]):
        plan = first + list(_plan)
        score = score_plan(plan)
        # print(plan, score)
        scores.append(score)

    ptwo = max(scores)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
