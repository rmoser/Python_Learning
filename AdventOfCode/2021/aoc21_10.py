# Advent of Code
year = 2021
day = 10

import numpy as np
import aocd

text0 = "[({(<(())[]>[[{[]{<()<>> "
_ = """"
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
text1 = aocd.get_data(day=day, year=year)

se = {"{": "}", "[": "]", "(": ")", "<": ">"}

invalid_scores = {')': 3, ']': 57, "}": 1197, '>': 25137}
incomplete_scores = {')': 1, ']': 2, "}": 3, '>': 4}
inverse = {'[': ']', '(': ')', '{': '}', '<': '>'}


def simplify(s):
    # print(s)
    while any(x in s for x in ['()', '{}', '[]', '<>']):
        s = s.replace('[]', '')
        s = s.replace('()', '')
        s = s.replace('{}', '')
        s = s.replace('<>', '')
        # print(s)

    return s


if __name__ == '__main__':
    text = text1
    text = text.strip().splitlines()

    invalid_score = 0
    incomplete_scores_list = list()

    for line in text:
        invalid = False
        s = simplify(line)
        for c in s:
            # Invalid strings
            if c in ']})>':
                score = invalid_scores[c]
                # print(f"Invalid: {c} = {score}")
                invalid_score += score
                invalid = True
                break

        if not invalid:
            score = 0
            total = 0
            for c in s[::-1]:
                # print(s, c)
                score = incomplete_scores[inverse[c]]
                total *= 5
                total += score
                # print(s, c, score, total)
            incomplete_scores_list.append(total)

    incomplete_score = sorted(incomplete_scores_list)[len(incomplete_scores_list) // 2]

    print(f"AOC {year} day {day}  Part One: {invalid_score}")

    print(f"AOC {year} day {day}  Part Two: {incomplete_score}")
