# Advent of Code
year = 2023
day = 6

import numpy as np
import aocd

text0 = """
Time:      7  15   30
Distance:  9  40  200
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    times = (int(i) for i in text[0].split()[1:])
    dists = (int(i) for i in text[1].split()[1:])

    races = zip(times, dists)

    time = int(''.join(text[0].split()[1:]))
    dist = int(''.join(text[1].split()[1:]))

    results = []
    for race in races:
        l = []
        for i in range(1, race[0]):
            if i * (race[0]-i) > race[1]:
                l.append(i)

        results.append(l)

    pone = np.prod([len(l) for l in results])

    print(f"AOC {year} day {day}  Part One: {pone}")

    roots = sorted(np.roots([-1, time, -dist]))
    #
    # ptwo = 0
    # for i in range(time):
    #     if roots[0] < i < roots[1]:
    #         ptwo += 1
    #
    # print(roots)

    ptwo = int(roots[1]) - int(roots[0])

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
