# Advent of Code
year = 2015
day = 2

import numpy as np
import aocd

text0 = "2x3x4\n1x1x10"
text1 = aocd.get_data(day=day, year=year)


def calc_paper(l, w, h):
    sides = [l * w, w * h, l * h]
    return 2 * sum(sides) + min(sides)


def calc_ribbon(l, w, h):
    sides = 2 * min([l+w, l+h, w+h])
    bow = l * w * h
    return sides + bow


if __name__ == '__main__':
    text = text1
    presents = [int(i) for x in text.splitlines() for i in x.split('x')]
    presents = np.array(presents).reshape([len(presents)//3, 3])
    # print(presents)

    paper = [calc_paper(*x) for x in presents]
    # print(paper)
    print(f"AOC {year} day {day}  Part One: {sum(paper)}")

    ribbon = [calc_ribbon(*x) for x in presents]
    print(f"AOC {year} day {day}  Part Two: {sum(ribbon)}")
