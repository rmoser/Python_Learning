# Advent of Code
year = 2018
day = 4

import numpy as np
import aocd
import pandas as pd

text0 = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    text.sort()

    insts = dict()
    for line in text:
        d, inst = line.split("]")
        d, t = d[1:].split()
        d = d[5:]
        _, m = (int(x) for x in t.split(":"))

        inst = inst.split()
        if inst[0] == "Guard":
            g = int(inst[1][1:])
            k = (g, d)
            if k not in insts:
                insts[k] = list()
            continue

        insts[k].append((m, inst[0] == "falls"))

    arr = np.zeros(shape=60, dtype=int)
    timecols = [str(x) for x in range(60)]
    df = pd.DataFrame(columns=["date", "guard", "time"] + timecols)
    for i in timecols:
        df[i] = df[i].astype(int)
    df.guard = df.guard.astype(int)

    for k, inst in insts.items():
        g, d = k
        # print(g, d, inst, "\n")
        arr[:] = False
        start = 0
        for m, i in inst:
            if i:
                start = m
            else:
                arr[start:m] = True
                start = 0
        if start:
            arr[start:60] = True

        # print(g, d, arr)
        df = df.append(pd.Series([g, d, arr.copy()] + list(arr), ["guard", "date", "time"] + timecols), ignore_index=True)

    df['sleep'] = df.time.apply(sum)

    guard = df[["guard", "sleep"]].groupby("guard").sum().idxmax()[0]

    asleep = df[["guard"] + timecols].groupby("guard").sum()

    t = np.argmax(asleep[asleep.index == guard].sum())

    pone = guard * t

    print(f"AOC {year} day {day}  Part One: {pone}")

    guards = asleep.max(axis='columns')
    guard = guards.idxmax()
    t = asleep[asleep.index == guard].max().idxmax()

    ptwo = guard * int(t)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
