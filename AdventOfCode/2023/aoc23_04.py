# Advent of Code
year = 2023
day = 4

import numpy as np
import aocd
import os
import functools
os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"

text0 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone = 0
    scores = dict()
    cards = dict()
    for line in text:
        card, nums = line.split(': ')

        _, card = card.split()
        card = int(card)

        wins, nums = ({int(i) for i in x.split()} for x in nums.split(" | "))
        cards[card] = len(wins & nums)
        pone += int(2 ** (cards[card] - 1))

    arr = np.ones(shape=len(cards)+1, dtype=int)
    arr[0]=0
    for card in cards:
        for i in range(1, cards[card]+1):
            arr[card+i] += arr[card]

    ptwo = arr.sum()


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
