# Advent of Code
year = 2019
day = 3

import numpy as np
import aocd

text0 = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
text1 = aocd.get_data(day=day, year=year)


def map_path(a):
    a_list = []
    coord = [0, 0]
    for inst in a:
        _dir = inst[0]
        _dist = int(inst[1:])
        for _ in range(_dist):
            if _dir == 'D':
                coord[1] -= 1
            elif _dir == 'U':
                coord[1] += 1
            elif _dir == 'L':
                coord[0] -= 1
            elif _dir == 'R':
                coord[0] += 1
            c = tuple(coord)
            a_list.append(c)

    return a_list


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    a = text[0].split(',')
    b = text[1].split(',')
    print(a, b)

    a_set = map_path(a)
    b_set = map_path(b)

    print(a_set)
    print(b_set)

    c_set = set(a_set) & set(b_set)

    pone = min([abs(x) + abs(y) for x, y in c_set])

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = 2 + min(a_set.index(c) + b_set.index(c) for c in c_set)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
