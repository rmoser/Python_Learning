# Advent of Code
year = 2018
day = 9

import numpy as np
import aocd
from collections import deque

text0 = """
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""
text1 = aocd.get_data(day=day, year=year)


def score(players, marbles, debug=False):
    l = deque([0])
    player = 0
    scores = deque([0] * players)
    cur = 0

    for i in range(1, marbles+1):
        # if i % 1000 == 0:
        #     print(f"\r{i}", end='')
        # n = len(l)

        if debug:
            for x in range(n):
                if x == cur:
                    print(f"({l[x]}) ", end='')
                else:
                    print(f"{l[x]} ", end='')
            print()

        if (i % 23) == 0:
            l.rotate(-7)
            s = i + l.pop()
            scores[player] += s
            # print(i, s)
        else:
            l.rotate(2)

            # if debug:
            #   print("ins: ", i, new, l)
            l.append(i)

        player = (player + 1) % players

    # print()
    return max(scores)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    if not isinstance(text, list):
        text = [text]

    for line in text:
        line = line.split()
        players = int(line[0])
        marbles = int(line[6])
        if len(line) > 10:
            ans = int(line[11])
        else:
            ans = 0

        result = score(players, marbles)
        if text == text0:
            print(f"{result} == {ans} ?  P: {players}  M: {marbles}")

        pone = result

    print(f"AOC {year} day {day}  Part One: {pone}")

    result = score(players, marbles * 100)
    ptwo = result

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
