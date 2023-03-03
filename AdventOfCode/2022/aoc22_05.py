# Advent of Code
year = 2022
day = 5

import numpy as np
import aocd
import copy

text0 = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
text1 = aocd.get_data(day=day, year=year)

def get_stacks(data):
    stacks = [list() for i in range(9)]
    for line in stacks_text:
        if line and line.strip()[0] == '[':
            chunks = [line[i:i+4].strip('[] ') for i in range(0, len(line), 4)]
            for i, c in enumerate(chunks):
                if c:
                    stacks[i].insert(0, c)
    return stacks


def cratemover_9000(s, inst_text):
    st = copy.deepcopy(s)
    for i, inst in enumerate(inst_text):
        if not inst:
            continue
        inst = inst.split()
        c = int(inst[1])
        f = int(inst[3]) - 1
        t = int(inst[5]) - 1

        for _ in range(c):
            st[t].append(st[f].pop())
    return st


def cratemover_9001(s, inst_text):
    st = copy.deepcopy(s)
    # print(-1, st)
    for i, inst in enumerate(inst_text):
        if not inst:
            continue
        inst = inst.split()
        c = int(inst[1])
        f = int(inst[3]) - 1
        t = int(inst[5]) - 1

        st[t] += (st[f][-1 * c:])
        st[f] = st[f][:-1 * c]
        # print(i, st, inst)
    return st


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    stacks_text, inst_text = (x.split('\n') for x in text.split('\n\n'))

    stacks = get_stacks(stacks_text)

    s9000 = cratemover_9000(stacks, inst_text)
    s9001 = cratemover_9001(stacks, inst_text)

    pone = ''.join(s[-1] for s in s9000 if s)
    ptwo = ''.join(s[-1] for s in s9001 if s)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
