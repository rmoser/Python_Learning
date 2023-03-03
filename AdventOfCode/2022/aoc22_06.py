# Advent of Code
year = 2022
day = 6

import numpy as np
import aocd

text0 = """bvwbjplbgvbhsrlpgdmjqwftvncz"""
text1 = aocd.get_data(day=day, year=year)


def find_packet(s):
    for i in range(len(s)):
        if len(set(s[i:i+4])) == 4:
            return i + 4


def find_message(s):
    for i in range(len(s)):
        if len(set(s[i:i+14])) == 14:
            return i + 14


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    pone = find_packet(text)
    ptwo = find_message(text)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
