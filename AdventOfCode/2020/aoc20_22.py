# Advent of Code
from logging import DEBUG

year = 2020
day = 22

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""
text1 = aocd.get_data(day=day, year=year)

DEBUG = False

def play1(p1, p2):
    while len(p1) > 0 and len(p2) > 0:
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if c1 > c2:
            p1 += [c1, c2]
        else:
            p2 += [c2, c1]

    if p1:
        return 0, p1
    return 1, p2


def play2(p1, p2, game=0):
    game += 1
    if DEBUG:
        print(f'\n=== Game {game} ===')
    hist = set()
    r = 0
    while len(p1) > 0 and len(p2) > 0:
        r += 1
        h = (tuple(p1), tuple(p2))
        if h in hist:
            return 0, p1
        hist.add(h)

        if DEBUG:
            print(f'\n-- Round {r} (Game {game}) --')
            print(f'Player 1\'s deck: {p1}')
            print(f'Player 2\'s deck: {p2}')

        c1 = p1.pop(0)
        c2 = p2.pop(0)

        if DEBUG:
            print(f'Player 1 plays: {c1}')
            print(f'Player 2 plays: {c2}')

        result = None
        if c1 <= len(p1) and c2 <= len(p2):
            if DEBUG:
                print(f'Playing a sub-game to determine the winner...')
            result, _ = play2(p1[:c1], p2[:c2], game+1)
            if DEBUG:
                print(f'\n...anyway, back to game {game}')

        if result == 0 or result is None and c1 > c2:
            if DEBUG:
                print(f'Player 1 wins round {r} of game {game}!')
            p1 += [c1, c2]
        elif result == 1 or result is None and c2 > c1:
            if DEBUG:
                print(f'Player 2 wins round {r} of game {game}!')
            p2 += [c2, c1]

    if p1:
        print(f'The winner of game {game} is player 1')
        return 0, p1

    print(f'The winner of game {game} is player 2')
    return 1, p2

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n')

    p1, p2 = text

    p1 = [int(x) for x in p1.splitlines()[1:]]
    p2 = [int(x) for x in p2.splitlines()[1:]]

    _, cards = play1(p1[:], p2[:])

    pone = sum((i+1) * v for i, v in enumerate(cards[::-1]))

    print(f"AOC {year} day {day}  Part One: {pone}")

    _, cards = play2(p1[:], p2[:])
    print(cards)
    ptwo = sum((i+1) * v for i, v in enumerate(cards[::-1]))
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
