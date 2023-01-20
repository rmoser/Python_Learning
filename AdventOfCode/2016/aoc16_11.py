# Advent of Code
year = 2016
day = 11

import numpy as np
import aocd
import itertools


text0 = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""
text1 = aocd.get_data(day=day, year=year)

elevator = [1, [None, None]]
FLOOR = 0
INSIDE = 1

BUILDING = [[], [], [], []]
ELEVATOR = 0


class Component:
    def __init__(self, name, _type, floor):
        self.name = name.replace('-compatible', '').replace('.', '')
        self.type = _type.replace('.', '')
        self.floor = floor

    def __repr__(self):
        return f'{self.type}: {self.name} on {self.floor}'


def show(label=''):
    print(f'\nBuilding state: {label}')
    for f in reversed(range(len(BUILDING))):
        print('floor: ', f+1, BUILDING[f])
    print()


def move(start, end, items):
    global BUILDING, ELEVATOR

    if ELEVATOR != start:
        return False
    if any(i.floor != start for i in items):
        return False
    if not is_valid_floor(items):
        return False
    if not any(i.type == 'microchip' for i in items):
        return False
    if not is_valid_floor(BUILDING[end] + items):
        return False

    # Everything ok, let's move
    for i in items:
        i.floor = end
        BUILDING[start].remove(i)
        BUILDING[end].append(i)
        ELEVATOR = end
    return True


def is_valid_floor(group):
    if not isinstance(group, list):
        raise TypeError(f"group should be a list, not a {type(group)}")
    if len(group) == 0:
        return True

    if all(i.type == 'microchip' for i in group):
        return True

    if all(i.type == 'generator' for i in group):
        return True

    for i in group:
        # Any microchip on a floor with at least one generator needs to have
        # it's specific generator to avoid being destroyed
        if i.type == 'microchip' and any(o.type == 'generator' and o.name == i.name for o in group):
            return True

    return False


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    for floor, line in enumerate(text):
        # print(line)

        x = line.split('contains ')[1]
        if x.startswith('nothing'):
            continue

        items = x.split(' and ')
        for i in items:
            # print('floor', i)
            _, n, t = i.split()
            BUILDING[floor].append(Component(n, t, floor))

    show()

    print('valid: ', [is_valid_floor(BUILDING[i]) for i in range(4)])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
