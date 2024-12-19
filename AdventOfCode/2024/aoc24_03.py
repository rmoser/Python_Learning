# Advent of Code
year = 2024
day = 3

import numpy as np
import aocd
import os
import re
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
text1 = aocd.get_data(day=day, year=year)

def score(string):
    result = re.findall(r"mul\((\d\d?\d?),(\d\d?\d?)\)", string)
    return sum((int(a) * int(b) for a, b in result))


if __name__ == '__main__':
    pone = 0
    ptwo = 0

    text = text1
    text = text.strip()

    new_text = re.sub(r"(don't\(\))", r"\t\1", "do()" + text)
    new_text = re.sub(r"(do\(\))", r"\t\1", new_text).split("\t")

    for line in new_text:
        s = score(line)
        pone += s
        if line.startswith('do()'):
            ptwo += s

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
