# Advent of Code
year = 2019
day = 6

import numpy as np
import aocd

text0 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""
text1 = aocd.get_data(day=day, year=year)


class Obj(object):
    objs = dict()

    def calc(self):
        for obj in Obj.objs.values():
            if isinstance(obj.orbit, str) and obj.orbit in Obj.objs:
                obj.orbit = Obj.objs[obj.orbit]

    def __init__(self, name, orbit):
        self.name = name
        if orbit in Obj.objs:
            self.orbit = Obj.objs[orbit]
        else:
            self.orbit = orbit
        self._level = 0
        self._chain = list()
        Obj.objs[name] = self

    def __repr__(self):
        return f"{self.name} ( {self.orbit if isinstance(self.orbit, str) else self.orbit.name}  L {self._level}"

    def level(self):
        if not self._level:
            if isinstance(self.orbit, Obj):
                self._level = 1 + self.orbit.level()
        return self._level

    def orbit_chain(self):
        if not self._chain:
            if isinstance(self.orbit, str) and self.orbit in self.objs:
                self.calc()
            if isinstance(self.orbit, Obj):
                self._chain = self.orbit.orbit_chain() + [self.name]
            else:
                self._chain = [self.name]
        return self._chain


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    com = Obj("COM", '')
    for line in text:
        a, b = line.split(")")
        _ = Obj(b, a)

    com.calc()
    pone = sum(x.level() for x in Obj.objs.values())
    print(f"AOC {year} day {day}  Part One: {pone}")

    you = com.objs['YOU'].orbit_chain()
    san = com.objs['SAN'].orbit_chain()

    while you[0] == san[0]:
        you = you[1:]
        san = san[1:]

    ptwo = len(you) + len(san) - 2
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
