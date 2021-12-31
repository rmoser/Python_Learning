# Advent of Code
year = 2015
day = 14

import numpy as np
import aocd

text0 = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    if text == text0:
        total_time = 1000
    else:
        total_time = 2503

    text = text.strip().splitlines()

    d = dict()
    for line in text:
        s = line.split()
        name = s[0]
        speed = int(s[3])
        flight = int(s[6])
        rest = int(s[-2])
        d[name] = (speed, flight, flight + rest)

    distance = dict()
    for name, info in d.items():
        q, r = divmod(total_time, info[2])
        distance[name] = info[0] * info[1] * (q + min(1, r/info[1]))

    pone = max(distance.values())
    print(f"AOC {year} day {day}  Part One: {pone}")

    n = len(d)
    speeds = np.array([x[0] for x in d.values()], dtype=int)
    flight = np.array([x[1] for x in d.values()], dtype=int)
    period = np.array([x[2] for x in d.values()], dtype=int)

    distances = np.zeros(shape=n, dtype=int)
    timers = np.zeros(shape=n, dtype=int)
    scores = np.zeros(shape=n, dtype=int)

    for i in range(total_time):
        timers += 1
        distances = distances + speeds * (timers <= flight)
        scores += (distances == distances.max())
        timers[timers >= period] = 0

    ptwo = scores.max()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
