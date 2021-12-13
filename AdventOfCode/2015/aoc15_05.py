# Advent of Code
year = 2015
day = 5

import numpy as np
import aocd

text0 = "ugknbfddgicrmopn\naddei\njchzalrnumimnmhp\nhaegwjzuvuyypxyu\ndvszwmarrgswjxmb"
text1 = "qjhvhtzxzqqjkmpb\nxxyxx\nuurcxstgmygtbstg\nieodomkazucvgmuy"
text2 = aocd.get_data(day=day, year=year)


def is_nice(s):
    # Avoid bad list
    for c in ('ab', 'cd', 'pq', 'xy'):
        if c in s:
            return False

    # >= 3 vowels
    if sum([c in 'aeiou' for c in s]) < 3:
        return False

    # Any repeated letter
    if not any([a == b for a, b in zip(s[:-1], s[1:])]):
        return False

    return True


def is_nice2(s):
    # Same letter with any letter in-between
    if not any([a == b for a, b in zip(s[:-2], s[2:])]):
        return False

    # Any repeating pair
    for a, b in zip(s[:-1], s[1:]):
        if s.count(a+b) > 1:
            return True

    return False


if __name__ == '__main__':
    text = text2
    text = text.splitlines()

    count_nice1 = sum([is_nice(x) for x in text])

    count_nice2 = sum([is_nice2(x) for x in text])
    for x in text:
        print(f"{x}: {is_nice2(x)}")

    print(f"AOC {year} day {day}  Part One: {count_nice1}")

    print(f"AOC {year} day {day}  Part Two: {count_nice2}")
