# Advent of Code
year = 2018
day = 7

import numpy as np
import aocd

text0 = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""
text1 = aocd.get_data(day=day, year=year)



if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    if text == text0:
        n_workers = 2
        base_t = 0
    else:
        n_workers = 5
        base_t = 60

    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    d = dict()
    for line in text:
        a = line[5]
        b = line[36]
        if a not in d:
            d[a] = set()
        if b not in d:
            d[b] = set()
        d[a].add(b)

    word = ''

    while d:
        nodes = set(d)
        for v in d.values():
            nodes -= v

        letter = sorted(nodes)[0]
        d.pop(letter)
        word += letter

    pone = word

    print(f"AOC {year} day {day}  Part One: {pone}")


    d = dict()
    for line in text:
        a = line[5]
        b = line[36]
        if a not in d:
            d[a] = set()
        if b not in d:
            d[b] = set()
        d[a].add(b)

    word = ''

    t = 0
    workers = np.zeros(shape=n_workers, dtype=int)
    z = workers.copy()
    status = np.zeros(shape=6, dtype=str)

    todo = set(d)

    while todo:
        # any open workers?
        for i in range(n_workers):
            if workers.min() == 0:
                i = workers.argmin()
                # Any nodes ready to be worked?
                nodes = todo - set(list(word))
                for v in d.values():  # Blocked
                    nodes -= v
                nodes -= set(status)  # In Work

                if nodes:
                    letter = sorted(nodes)[0]
                    workers[i] += base_t + ord(letter) - 64
                    status[i] = letter


        # Increment time and process outcomes
        t += 1
        workers = np.maximum(z, workers-1)
        for i in range(n_workers):
            if workers[i] == 0 and status[i]:
                word += status[i]
                todo.remove(status[i])
                d.pop(status[i])
                status[i] = ''

        # print(t, workers, status, d)
        # print(word)

    ptwo = t






    print(f"AOC {year} day {day}  Part Two: {ptwo}")
