# Advent of Code
year = 2015
day = 8

import numpy as np
import aocd

text0 = '""\n"abc"\n"aaa\\"aaa"\n"\\x27"'
text1 = aocd.get_data(day=day, year=year)


def tokens(s):
    iterator = iter(s)
    for char in iterator:
        if char == "\\":
            char += next(iterator)
            if char.endswith("x"):
                char += next(iterator)
                char += next(iterator)
        yield char


def encode(s):
    iterator = iter(s)
    for char in iterator:
        if char == '\\':
            char = r'\\'
        if char == '"':
            char = r'\"'
        yield char


if __name__ == '__main__':
    text = text1.splitlines()

    n_tokens = sum(1 for s in text for t in tokens(s)) - 2 * len(text)
    n_encodes = sum(len(x) for s in text for x in encode(s)) + 2 * len(text)
    n_chars = sum(len(s) for s in text)

    # text = text.replace(b"\\", b"\\\\").replace("\"", b"\\\"")

    # for i in range(5):
    #     t = text[i]
    #     print(f"strings {len(t)}: {t}")
    #     tok = list(encode(t))
    #     print(f"encodes {sum(len(x) for x in tok)+2}: {tok}")




    print(f"AOC {year} day {day}  Part One: {n_chars - n_tokens}")

    print(f"AOC {year} day {day}  Part Two: {n_encodes - n_chars}")
