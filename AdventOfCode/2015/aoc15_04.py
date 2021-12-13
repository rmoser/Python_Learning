# Advent of Code
year = 2015
day = 4

import numpy as np
import hashlib as hl
import aocd

text0 = "abcdef"
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    text = text1

    def get_hash(s, digits):
        md5 = hl.md5(s.encode())
        i = 0
        digest = "11111"
        while digest[:digits] != '0' * digits:
            md5c = md5.copy()
            md5c.update(str(i).encode())
            digest = md5c.hexdigest()
            i += 1

        i -= 1

        return i, digest


    i, digest = get_hash(text, 5)
    print(f"AOC {year} day {day}  Part One: {i} {digest}")

    i, digest = get_hash(text, 6)
    print(f"AOC {year} day {day}  Part Two: {i} {digest}")
