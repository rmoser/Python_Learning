# Advent of Code
year = 2016
day = 14

import numpy as np
import aocd
import hashlib

text0 = "abc"

text1 = aocd.get_data(day=day, year=year)

HASHES = []


def just_hash(i, text):
    return hashlib.md5(f"{text}{i}".encode()).hexdigest().lower()


def just_hash2(i, text):
    h = just_hash(i, text)
    for _ in range(2016):
        h = hashlib.md5(h.encode()).hexdigest()

    return h


def get_hash(i, text, pone=True):
    if i < len(HASHES) and HASHES[i]:
        return HASHES[i]

    while len(HASHES) < i+1:
        HASHES.append('')

    if pone:
        h = just_hash(i, text)
    else:
        h = just_hash2(i, text)

    triples, quints = triplets_and_quints(h)

    HASHES[i] = triples, quints
    return HASHES[i]


def triplets_and_quints(h):
    triplets = [a for a, b, c in zip(h[:-2], h[1:-1], h[2:]) if a == b and b == c]
    if triplets:
        t = triplets[0]
        t_set = set(t)
        q = set([t for t in triplets if t*5 in h])
        return t_set, q
    return set(), set()


def fill_hash(i, text, pone=True):
    for j in range(len(HASHES), i+1001):
        get_hash(j, text, pone)


def update_hashes():
    for i in range(len(HASHES)-1000):
        h = HASHES[i]
        if len(h) < 3:
            quints = set([c for q in HASHES[i+1:i+1001] for c in q[1]])
            HASHES[i] = tuple(list(HASHES[i]) + [quints])


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    i = 0
    keys = []

    end = 64

    while True:
        fill_hash(i+1001, text)
        update_hashes()
        if HASHES[i][0] & HASHES[i][2]:
            keys.append(i)

        if len(keys) >= end:
            break
        if i > 25000:
            break
        i += 1
        if i % 1000 == 0:
            print(f"\r{i} {len(keys)}", end="")

    print('\r', end='')
    pone = keys[-1]
    print(f"AOC {year} day {day}  Part One: {pone}")


    i = 0
    keys = []
    HASHES = []

    end = 64
    while True:
        fill_hash(i+1001, text, pone=False)
        update_hashes()
        if HASHES[i][0] & HASHES[i][2]:
            keys.append(i)

        if len(keys) >= end:
            break
        if i > 40000:
            break
        i += 1
        if i % 1000 == 0:
            print(f"\r{i} {len(keys)}", end="")

    print('\r', end='')
    ptwo = keys[-1]
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
