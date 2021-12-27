# Advent of Code
year = 2021
day = 22

import numpy as np
import aocd
import itertools

text0 = """
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""
text1 = aocd.get_data(day=day, year=year)


class Rect:
    def __init__(self, c0, c1):
        self.c = np.array([c0, c1])
        self.c0 = tuple(self.c.min(axis=0))
        self.c1 = tuple(self.c.max(axis=0))

        self._shape = tuple(self.c.max(axis=0)-self.c.min(axis=0))
        self.corners = frozenset(itertools.product(*self.c.T))

    def __contains__(self, coord):
        return all(self.c0[i] <= coord[i] <= self.c1[i] for i in range(3))

    def __hash__(self):
        return self.corners.__hash__()

    def __eq__(self, other):
        return self.corners == other.corners

    def intersects(self, other):
        if any(c in self for c in other.corners):
            return True
        if any(c in other for c in self.corners):
            return True
        return False

    def is_inside(self, coord):
        return np.array([self.c[0] < coord, coord < self.c[1]]).all()

    def is_onface(self, coord):
        return coord in self and np.array([self.c[0] == coord, coord == self.c[1]]).any()

    def is_onedge(self, coord):
        return coord in self and np.array([self.c[0] == coord, coord == self.c[1]]).sum() >= 2

    def is_corner(self, coord):
        return coord in self.corners

    def adjoins(self, other):
        return sum(self.corners & other.corners) >= 4

    def fracture(self, x):
        if isinstance(x, tuple):
            if x in self.corners:
                return {self}

            if x in self:
                return set([i for i in [Rect(c, x) for c in self.corners] if i.volume()])
            return {}

        elif isinstance(x, Rect):
            coords = set(c for c in x.corners if c in self)
            print("Rect fracture coords: ", coords)
            a = [Rect(self.c0, self.c1)]
            for c in coords:
                a = [i for r in a for i in r.fracture(c)]

            return set([x for x in a if x.volume()])

    def shape(self):
        return self._shape

    def volume(self):
        return np.product(self._shape)

    def __str__(self):
        return f"Rect({self.c0}, {self.c1})"

    def __repr__(self):
        return self.__str__()


def apply(inst, arr):
    on, ((x0, xn), (y0, yn), (z0, zn)) = inst

    if any((-50 > c or 50 < c) for c in (x0, xn, y0, yn, z0, zn)):
        return arr, 0

    coords = set(itertools.product(range(x0, xn+1), range(y0, yn+1), range(z0, zn+1)))

    if on:
        new_arr = arr | coords
        return new_arr, len(new_arr - arr)
    else:
        new_arr = arr - coords
        return new_arr, -len(arr - new_arr)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    if False:
        instructions = [line.split() for line in text]
        for line in instructions:
            line[0] = line[0] == 'on'
            xyz = [inst[2:].split("..") for inst in line[1].split(',')]
            line[1] = tuple(tuple(int(i) for i in coord) for coord in xyz)

        xyz = np.array([line[1] for line in instructions])

        xyz_range = np.array([xyz.min(axis=(0, 2)), xyz.max(axis=(2, 0))]).T

        offset = -1 * np.array(xyz_range[:, 0])
        shape = xyz_range[:, 1] + offset + 1

        arr = np.zeros(shape=shape, dtype=np.bool)

        for i, inst in enumerate(instructions):
            arr, delta = apply(inst, arr)
            print(i, delta)

        pone = len(arr)

        print(f"AOC {year} day {day}  Part One: {pone}")

        print(f"AOC {year} day {day}  Part Two: {ptwo}")

    a = Rect((0, 0, 0), (4, 4, 4))
    b = Rect((1, 1, 1), (3, 3, 3))

    c = a.fracture((0, 1, 1))
    d = a.fracture(b)
    print(d)
    print(len(d))
