# Advent of Code
year = 2020
day = 25

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
17807724
5764801
"""
text1 = aocd.get_data(day=day, year=year)

def transform(val, subject, loops):
    for _ in range(loops):
        val *= subject
        val %= 20201227
    return val

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    door, card = [int(x) for x in text]

    door_loop = 0
    card_loop = 0
    i = 0
    num = 1
    subject = 7
    while door_loop == 0 or card_loop == 0:
        i += 1
        num = transform(num, subject, 1)
        if num == door:
            door_loop = i
        if num == card:
            card_loop = i


    door_key = transform(1, card, door_loop)
    card_key = transform(1, door, card_loop)

    if door_key == card_key:
        pone = door_key

    # print(door, card)
    # for l in range(30):
    #     door = transform(door, l)
    #     card = transform(card, l)
    #     print(door, card)


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
