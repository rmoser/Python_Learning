# Advent of Code
year = 2016
day = 21

import numpy as np
import aocd
import itertools

text0 = """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""
text1 = aocd.get_data(day=day, year=year)


def rotate_right(s, n):
    return s[-n:] + s[:-n]


def rotate_left(s, n):
    return s[n:] + s[:n]


def rotate_right_based(s, a):
    if isinstance(s, str):
        idx = s.find(a)
    else:
        idx = s.index(a)
    n = (idx + 1 + (idx >= 4)) % len(s)
    return rotate_right(s, n)


def unrotate_right_based(s, a):
    for i in list(range(len(s))):
        x = rotate_left(s, i)
        if rotate_right_based(x, a) == s:
            return x


def swap(s, a, b):
    if isinstance(a, str) and a.isnumeric():
        a = int(a)
    if isinstance(b, str) and b.isnumeric():
        b = int(b)

    if isinstance(s, str):
        _s = list(s)
    else:
        _s = s.copy()

    if isinstance(a, str):
        a = s.index(a)
        b = s.index(b)

    _s[a], _s[b] = _s[b], _s[a]  # Swap chars

    if isinstance(s, str):
        return ''.join(_s)
    else:
        return _s


def reverse(s, a, b):
    return s[:a] + s[a:b + 1][::-1] + s[b + 1:]


def move(s, a, b):
    _s = list(s).copy()
    _a = _s[a:a + 1]
    _s = _s[:a] + _s[a + 1:]
    _s = _s[:b] + _a + _s[b:]

    if isinstance(s, str):
        return ''.join(_s)
    return _s


def scramble(password, instructions):
    password = list(password)

    for line in instructions:
        line = line.split()

        if line[0] == 'swap':
            password = swap(password, line[2], line[5])

        elif line[0] == 'rotate':
            if line[1] == 'left':
                n = int(line[2])
                password = rotate_left(password, n)
            elif line[1] == 'right':
                n = int(line[2])
                password = rotate_right(password, n)
            elif line[1] == 'based':
                a = line[-1]
                password = rotate_right_based(password, a)

        elif line[0] == 'reverse':
            a, b = int(line[2]), int(line[4])
            password = reverse(password, a, b)

        elif line[0] == 'move':
            a, b = int(line[2]), int(line[5])
            password = move(password, a, b)

        # print(password, line)

    return ''.join(password)


def unscramble(password, instructions):
    password = list(password)

    for line in instructions[::-1]:
        line = line.split()

        if line[0] == 'swap':
            password = swap(password, line[2], line[5])

        elif line[0] == 'rotate':
            if line[1] == 'right':
                n = int(line[2])
                password = rotate_left(password, n)
            elif line[1] == 'left':
                n = int(line[2])
                password = rotate_right(password, n)

            elif line[1] == 'based':
                a = line[-1]
                for i in range(len(password)):
                    s = rotate_left(password, i)
                    if rotate_right_based(s, a) == password:
                        password = s

        elif line[0] == 'reverse':
            a, b = int(line[2]), int(line[4])
            password = reverse(password, a, b)

        elif line[0] == 'move':
            a, b = int(line[2]), int(line[5])
            password = move(password, b, a)

        # print(password, line)

    return ''.join(password)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    instructions = list(text.strip().splitlines())

    if text == text0:
        password = 'abcde'
    else:
        password = 'abcdefgh'

    trace1 = [['', password, '']]
    for line in instructions:
        i = trace1[-1][1]
        o = scramble(i, [line])
        trace1.append([i, o, line])

    password = trace1[-1][1]

    pone = ''.join(password)

    print(f"AOC {year} day {day}  Part One: {pone}")

    # for i, o, line in trace1[:0:-1]:
    #     if unscramble(o, [line]) != i:
    #         print("error with unscramble: ", o, i, line)

    ptwo = 'fbgdceah'
    result = []
    for pw in itertools.permutations(ptwo):
        _pw = ''.join(pw)
        if scramble(_pw, instructions) == ptwo:
            result.append(_pw)

    ptwo = result[-1]
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
