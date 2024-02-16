# Advent of Code
year = 2023
day = 1

import numpy as np
import aocd

text0 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
text0 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    nums = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

    s1, s2 = 0, 0
    for line in text:
        l1 = [c for c in line if c.isnumeric()]
        if l1:
            s1 += int(l1[0] + l1[-1])

        l2 = []
        for i, c in enumerate(line):
            if c.isnumeric():
                l2.append(c)
                continue

            for num in nums:
                if line[i:i+len(num)] == num:
                    l2.append(nums[num])
        # print(l2)

        s2 += int(l2[0] + l2[-1])

    pone = s1
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = s2
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
