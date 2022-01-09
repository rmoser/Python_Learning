# Advent of Code
year = 2016
day = 15

import numpy as np
import aocd

text0 = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""
text1 = aocd.get_data(day=day, year=year)

# Dirty Enums
RANK = 0
START = 1
PERIOD = 2


def valid_state(i, discs):
    result = True
    for n, start, period in discs:
        result &= (start + i + n) % period == 0
    return result

def next_valid_state(discs):
    # Time-adjust for delay between button-press and when the ball reaches each disc
    d = [[n, (start + n) % period, period] for n, start, period in discs]

    discs = d.copy()

    result = 0
    mult = 1
    for disc in discs[::-1]:
        remainder = (disc[PERIOD] - disc[START] - result) % disc[PERIOD]
        print(disc, remainder)
        for i in range(1, disc[PERIOD]+1):
            if (i * mult) % disc[PERIOD] == remainder:
                result += i * mult
                mult *= disc[PERIOD]
                break
        print(result, mult, disc)

    return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    discs = []

    for line in text:
        line = line.split()
        n = int(line[1][1:])
        period = int(line[3])
        start = int(line[-1][:-1])
        discs.append([n, start, period])

    print("Discs: ", discs)

    pone = next_valid_state(discs)
    print(f"AOC {year} day {day}  Part One: {pone}")

    discs.append([7, 0, 11])
    ptwo = next_valid_state(discs)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
