# Advent of Code
year = 2019
day = 13

import numpy as np
import aocd
import itertools as it

text0 = """1,2,3,6,5,4"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()
    arr = [int(x) for x in text.split(',')]
    board = {}
    for job in it.batched(arr, 3):
        if len(job) < 3:
            continue
        x, y, i = job
        if not i in board:
            board[i] = set()
        board[i].add((x, y))

    pone = len(board[2])


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
