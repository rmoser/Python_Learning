# Advent of Code
year = 2016
day = 8

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)


def show(screen):
    print(f"  {''.join(str(s) for s in range(10)) * 5}")
    for r in range(screen.shape[0]):
        # print(f"{r}", ''.join(screen[r].astype(str)).replace('0', '\u25AF').replace('1', '\u25AE'))
        print(f"{r}", ''.join(screen[r].astype(str)).replace('0', ' ').replace('1', '#'))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    screen = np.zeros(shape=(6, 50), dtype=int)

    for line in text:
        words = line.split()
        if line.startswith('rect'):
            c, r = (int(x) for x in words[1].split('x'))
            screen[:r, :c] = 1
            continue
        if line.startswith('rotate row'):
            n = int(words[-1])
            r = words[-3].split('=')[1]
            r = int(r)
            screen[r, :] = np.append(screen[r, -n:], screen[r, :-n])
            continue
        if line.startswith('rotate column'):
            n = int(words[-1])
            c = words[-3].split('=')[1]
            c = int(c)
            screen[:, c] = np.append(screen[-n:, c], screen[:-n, c])
            continue

    pone = screen.sum()

    show(screen)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
