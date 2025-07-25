# Advent of Code
from scipy.stats import false_discovery_control

year = 2024
day = 9

import numpy as np
import aocd
import os
import itertools as it
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """2333133121414131402"""
text1 = aocd.get_data(day=day, year=year)

def clean(filesys):
    for i in range(len(filesys)-1, -1, -1):
        if filesys[i][1] == 0:
            filesys.pop(i)
    while filesys[-1][0] is None:
        filesys.pop(-1)
    if filesys[-2][0] is None:
        filesys.pop(-2)
    return filesys

def is_defragged(filesys):
    for b, n in filesys:
        if b is None:
            return False
    return True

def defrag1(filesys):
    clean(filesys)

    for i, (blk, blk_count) in enumerate(filesys):
        if blk is None:
            new_blk, new_blk_count = filesys[-1]
            if blk_count <= new_blk_count:
                filesystem[i] = (new_blk, blk_count)
                filesystem[-1] = (new_blk, new_blk_count - blk_count)
            else:
                filesys.insert(i, (new_blk, new_blk_count))
                filesys[i+1] = (blk, blk_count - new_blk_count)
                filesys.pop(-1)
            break

def clean2(filesys):
    # for i in range(len(filesys)-1, -1, -1):
    #     if filesys[i][1] == 0:
    #         filesys.pop(i)

    for i in range(len(filesys)-1, -1, -1):
        a = filesys[i-1]
        b = filesys[i]
        if a[0] == b[0]:
            filesys[i-1] = (a[0], a[1]+b[1])
            filesys.pop(i)

    # while filesys[-1][0] is None:
    #     filesys.pop(-1)
    return filesys


def defrag2(filesys, b):
    clean2(filesys)

    for n, (new_blk, new_blk_count) in enumerate(filesys):
        if new_blk != b:
            continue
        break

    for i, (blk, blk_count) in enumerate(filesys):
        if i < n and blk is None:
            if blk_count == new_blk_count:
                filesys[i] = (new_blk, new_blk_count)
                filesys[n] = (None, blk_count)
                break

            if blk_count > new_blk_count:
                filesys.insert(i, (new_blk, new_blk_count))
                filesys[i+1] = (None, blk_count - new_blk_count)
                filesys[n+1] = (None, new_blk_count)
                break


def is_defragged2(filesys):
    for i, (b, n) in enumerate(filesys):
        if b is None:
            if any(c <= n for _, c in filesys[i+1:]):
                return False
    return True

def checksum(filesys):
    pos = -1
    result = 0
    for blk, count in filesystem:
        for _ in range(count):
            pos += 1
            result += pos * (blk if blk else 0)
    return result

def show(filesys):
    print(''.join(('.' if c is None else str(c)) * n for c, n in filesys))

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    filesystem = []
    for i, c in enumerate(text):
        if i % 2:
            filesystem.append((None, int(c)))
        else:
            filesystem.append((i//2, int(c)))

    while not is_defragged(filesystem):
        defrag1(filesystem)
    pone = checksum(filesystem)

    filesystem = []
    for i, c in enumerate(text):
        if i % 2:
            filesystem.append((None, int(c)))
        else:
            filesystem.append((i//2, int(c)))

    # show(filesystem)
    clean2(filesystem)
    # show(filesystem)
    for i in range(filesystem[-1][0], -1, -1):
        defrag2(filesystem, i)
        # print(i)
        # show(filesystem)

    # show(filesystem)
    ptwo = checksum(filesystem)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
