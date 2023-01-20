# Advent of Code
year = 2017
day = 9

import numpy as np
import aocd

text0 = """
{}
{{{}}}
{{},{}}
{{{},{},{{}}}}
{<a>,<a>,<a>,<a>}
{{<ab>},{<ab>},{<ab>},{<ab>}}
{{<!!>},{<!!>},{<!!>},{<!!>}}
{{<a!>},{<a!>},{<a!>},{<ab>}}
"""

text1 = aocd.get_data(day=day, year=year)


def remove_comments(text):
    # Remove comments
    new_text = ''
    i = 0
    while i < len(text):
        c = text[i]
        if c == '!':
            i += 2
            continue
        new_text += c
        i += 1

    return new_text


def remove_garbage(text):
    if len(text) == 0:
        return ''

    # print(0, text)
    text = ''.join([c for c in text if c in '{}<>,'])

    # print(1, text)
    new_text = ''
    comnt = False
    for c in text:
        if comnt:
            if c == '>':
                comnt = False
                new_text += c
        elif c == '<':
            comnt = True
            new_text += c
        else:
            new_text += c

    text = new_text

    return text


def reduce(text):
    if len(text) == 0:
        return ''

    # print(0, text)
    text = ''.join([c for c in text if c in '{}<>,'])

    # print(1, text)
    new_text = ''
    comnt = False
    for c in text:
        if comnt:
            if c == '>':
                comnt = False
        elif c == '<':
            comnt = True
        else:
            new_text += c


    text = new_text
    # print(2, text)

    return text


def score(text):
    total = 0
    level = 0
    for c in text:
        if c == '{':
            level += 1
        elif c == '}':
            total += level
            level -= 1
    return total


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    # print(text)

    for line in text:
        line0 = remove_comments(line)
        line1 = remove_garbage(line0)
        ptwo = len(line0) - len(line1)
        line2 = reduce(line1)
        pone = score(line2)
        print(line, pone)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
