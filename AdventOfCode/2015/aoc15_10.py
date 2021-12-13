# Advent of Code
year = 2015
day = 10

import numpy as np
import aocd

text0 = "111221"
text1 = aocd.get_data(day=day, year=year)


def proc(text):
    text_mod = "".join([a + ("" if a == b else " ") for a, b in zip(text[:-1], text[1:])]) + text[-1]
    text_mod2 = text_mod.split()

    return "".join([str(len(t)) + t[0] for t in text_mod2])


if __name__ == '__main__':
    text = text1

    t = text
    for i in range(40):
        t = proc(t)

    print(f"AOC {year} day {day}  Part One: {len(t)}")

    for i in range(10):
        t = proc(t)

    print(f"AOC {year} day {day}  Part Two: {len(t)}")
