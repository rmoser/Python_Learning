# Advent of Code
year = 2019
day = 8

import numpy as np
import aocd
import utils

text0 = """123456789012"""
text0 = "0222112222120000"
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    if text == text0:
        shape = (2, 2)
    else:
        shape = (6, 25)
    shape = (len(text) // (shape[0] * shape[1]),) + shape
    img = np.array([int(x) for x in text]).reshape(shape)

    i = (img == 0).sum(axis=(1, 2)).argmin()

    pone = (img[i] == 1).sum() * (img[i]==2).sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    idx = np.argmin(img==2, axis=0)
    img2 = np.array([img[i] * (idx == i) for i in range(img.shape[0])]).sum(axis=0)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
    utils.show(img2)
