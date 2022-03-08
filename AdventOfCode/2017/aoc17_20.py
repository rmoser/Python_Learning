# Advent of Code
year = 2017
day = 20

import numpy as np
import aocd

text0 = """
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
"""
text1 = aocd.get_data(day=day, year=year)

POS = 0
VEL = 1
ACC = 2


def step(particles):
    particles[:, VEL] += particles[:, ACC]
    particles[:, POS] += particles[:, VEL]


def dist(particles):
    return np.abs(particles[:, POS]).sum(axis=1)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    particles = np.zeros((len(text), 3, 3), dtype=int)
    mask = np.ones(len(text), dtype=bool)

    for i, line in enumerate(text):
        particle = np.array([y.split('<')[1].strip().split(',') for y in line.split('>') if y], dtype=int)
        particles[i] = particle

    for _ in range(1000):
        for i, particle in enumerate(particles):
            if not mask[i]:
                continue
            collisions = (particle[POS] == particles[:, POS]).all(axis=1).nonzero()[0]
            if len(collisions) > 1:
                for i in collisions:
                    mask[i] = False
        step(particles)

    pone = dist(particles).argmin()
    ptwo = mask.sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
