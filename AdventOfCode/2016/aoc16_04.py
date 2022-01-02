# Advent of Code
year = 2016
day = 4

import numpy as np
import aocd

text0 = """
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""
text1 = aocd.get_data(day=day, year=year)


def valid(name, checksum):
    chars, counts = np.unique(sorted(list(name.replace(' ', ''))), return_counts=True)

    ordered = np.concatenate([np.extract(counts == i, chars) for i in np.unique(counts)[::-1]]).flatten()

    return checksum == ''.join(ordered[:5])


def decrypt(name, n):
    return ''.join([chr(((ord(c) - 97 + n) % 26) + 97) if 97 <= ord(c) <= 122 else c for c in name])


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    rooms = dict()
    total = 0
    for line in text:
        words = line.split('-')
        id_cs = words[-1]
        name = ' '.join(words[:-1])

        id, cs = id_cs.replace(']', '').split('[')
        id = int(id)

        if valid(name, checksum=cs):
            total += id
            rooms[decrypt(name, id)] = id

    for k, v in rooms.items():
        if 'north' in k:
            ptwo = v

    pone = total

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
