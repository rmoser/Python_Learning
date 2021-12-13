# Advent of Code 2021
# Day 2

import aocd
day = 2
text1 = aocd.get_data(day=day, year=2021)

cmds = text1
cmds = cmds.split()
cmds = list(zip(cmds[::2], cmds[1::2]))

h, d = 0, 0

for cmd, n in cmds:
    if cmd == 'forward':
        h += int(n)
        continue
    if cmd == 'down':
        d += int(n)
        continue
    if cmd == 'up':
        d -= int(n)
        continue

print(f"Part 1: h, d: {h, d}")

print(h * d)


h, d, a = 0, 0, 0

for cmd, n in cmds:
    n = int(n)
    if cmd == 'forward':
        h += n
        d += a * n
        continue
    if cmd == 'down':
        a += n
        continue
    if cmd == 'up':
        a -= n
        continue

print(f"Part 2: h, d, a: {h, d, a}")

print(h * d)


