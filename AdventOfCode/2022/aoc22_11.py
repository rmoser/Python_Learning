# Advent of Code
year = 2022
day = 11

import numpy as np
import aocd
import math

text0 = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
text1 = aocd.get_data(day=day, year=year)


class Monkey(object):
    def __init__(self, n, items=None, operation=None, divisor=0, t=-1, f=-1):
        self.n = n
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.t = t
        self.f = f
        self.counter = 0

    def op(self, value):
        if self.operation[0] == '+':
            return value + self.operation[1]
        if self.operation[0] == '*':
            return value * self.operation[1]
        if self.operation[0] == '**':
            return value ** 2
        else:
            raise ValueError


def show(_monkeys):
    for m in _monkeys:
        print(f"{m.n}: {', '.join(str(x) for x in m.items)}")


def run(_monkeys, rounds, ratio, debug=False, denom=1):
    for r in range(rounds):
        if debug:
            print(f"\nRound {r}")
            show(_monkeys)
        else:
            print(f"\rRound {r}...", end='')
        for m in _monkeys:
            # m.items = list(map(m.op, m.items))
            #
            # if ratio == 3:
            #     m.items = [x // 3 for x in m.items]
            #
            # m.items = [x % denom for x in m.items]

            while m.items:
                i = m.items.pop(0)
                m.counter += 1
                new = m.op(i)
                if debug == 2:
                    print(f"m: {m.n}  i: {i}  new: {new}", end='')

                if ratio > 1:
                    new //= 3

                if denom > 1:
                    new %= denom

                result = (new % m.divisor) == 0

                if result:
                    # print(f'old: i  new: {new} to monkey {m.t}')
                    _monkeys[m.t].items.append(new)
                    if debug == 2:
                        print(f" -> {m.t}")
                else:
                    # print(f'old: i  new: {new} to monkey {m.f}')
                    _monkeys[m.f].items.append(new)
                    if debug == 2:
                        print(f" -> {m.f}")

    if debug:
        print(f"\nRound {r}")
        show(_monkeys)

    print('')
    return _monkeys


def read(text):
    coll = []
    for line in text:
        if ":" not in line:
            continue

        cmd = line.split(":")

        if cmd[0].startswith("Monkey"):
            n = cmd[0]
            m = Monkey(n)
            continue

        if cmd[0] == '  Starting items':
            m.items = [int(x) for x in cmd[1].split(', ')]
            continue

        if cmd[0] == '  Operation':
            eqn = cmd[1].split("=")[1]
            if '+' in eqn:
                args = eqn.split(' + ')
                m.operation = ('+', int(args[-1]))
            elif '*' in eqn:
                args = eqn.split(' * ')
                if args[-1] == 'old':
                    m.operation = ('**', None)
                else:
                    m.operation = ('*', int(args[-1]))
            continue

        if cmd[0] == '  Test':
            m.divisor = int(cmd[1].split()[-1])
            F.add(m.divisor)

        if cmd[0] == "    If true":
            m.t = int(cmd[1][-1])
            continue

        if cmd[0] == "    If false":
            m.f = int(cmd[1][-1])
            coll.append(m)

            m = None
            continue

    return coll


F = set()


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    # Init
    m = None

    monkeys = read(text)
    denom = 1
    monkeys = run(monkeys, 20, 3, 2, denom)
    counters = sorted([m.counter for m in monkeys])[-2:]
    pone = math.prod(counters)

    print(f"AOC {year} day {day}  Part One: {pone}")

    # exit()
    monkeys = read(text)
    denom = math.prod(F)
    monkeys = run(monkeys, 10000, 1, False, denom)
    counters = sorted([m.counter for m in monkeys])[-2:]
    ptwo = math.prod(counters)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
