# Advent of Code
year = 2018
day = 12

import numpy as np
import aocd

text0 = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    state = text[0][15:]

    insts = dict()
    for inst in text[2:]:
        a, _, c = inst.split()
        insts[a] = c

    start = 0
    for j in range(1, 10001):
        state = '....' + state + '....'
        start -= 2
        newstate = ''
        for i in range(2, len(state)-3):
            substr = state[i-2:i+3]
            if substr in insts:
                newstate += insts[substr]
            else:
                newstate += '.'

        # print("Old State: ", state)
        # state = newstate
        # print("New State: ", state)
        while newstate[0] == '.':
            # print('drop')
            start += 1
            newstate = newstate[1:]
        newstate = newstate.rstrip('.')
        if newstate == state:
            break

        state = newstate

        plants = [i for i, x in enumerate(state) if x == '#']
        score = sum(plants) + start * len(plants)

        # print(j, score, newstate)

        if j == 20:
            pone = score


    plants = [i for i, x in enumerate(state) if x == '#']
    s10k = sum(plants) + start * len(plants)
    s50b = (s10k - 466) // 10 * 50000000 + 466
    ptwo = s50b

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
