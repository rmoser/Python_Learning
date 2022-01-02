# Advent of Code
year = 2016
day = 7

import numpy as np
import aocd

text0 = """
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""
text1 = aocd.get_data(day=day, year=year)


def abba(s):
    for a, b in zip(zip(s[:-3], s[3:]), zip(s[1:-2], s[2:-1])):
        if a[0] == a[1] and b[0] == b[1] and a[0] != b[0]:
            return True
    return False


def ssl(aba, bab):
    ab_list = []
    for w in aba:
        for s in zip(w[:-2], w[2:], w[1:-1]):
            if s[0] == s[1] and s[0] != s[2]:
                ab_list.append(s[2] + s[0] + s[2])

    if any(ab in s for ab in ab_list for s in bab):
        return True
    return False


def parse(s):
    abba_good = []
    abba_bad = []
    start = 0
    i = 0
    in_brackets = False
    for i, c in enumerate(s):
        if c == '[':
            in_brackets = True
            if i:
                abba_good.append(s[start:i])
            start = i + 1
            continue

        if c == ']':
            abba_bad.append(s[start:i])
            in_brackets = False
            start = i+1
            continue

    if start < i:
        abba_good.append(s[start:])

    return abba_good, abba_bad


if __name__ == '__main__':
    text = text1
    text = text.strip().splitlines()

    pone = 0
    ptwo = 0
    for line in text:
        abba_good, abba_bad = parse(line)

        if any(abba(s) for s in abba_good) and not any(abba(s) for s in abba_bad):
            pone += 1

        if ssl(abba_good, abba_bad):
            ptwo += 1
        # print(line, pone)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
