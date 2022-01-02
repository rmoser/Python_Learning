# Advent of Code
year = 2016
day = 10

import numpy as np
import aocd

text0 = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""
text1 = aocd.get_data(day=day, year=year)

WAIT = True


class Bot:
    global WAIT

    def __init__(self, name, lo, hi, bots):
        self.name = name
        self.lo = lo
        self.hi = hi
        self.bins = []
        self.bots = bots
        if self.name.startswith('output'):
            self.type = 1
        else:
            self.type = 2

    def __repr__(self):
        return f"Bot {self.name}: [{', '.join([str(x) for x in self.bins])}]  lo: {self.lo}  hi: {self.hi}"

    def add(self, n):
        if self.type == 1:
            self.bins = [n]
        else:
            self.bins.append(n)

        if 61 in self.bins and 17 in self.bins:
            print(f"Bot {self.name} has chips 61 and 17!!!")

        if not WAIT:
            self.update()
        return True

    def update(self):
        if len(self.bins) == 2:
            lo = self.bots[self.lo]
            hi = self.bots[self.hi]

            lo.add(min(self.bins))
            hi.add(max(self.bins))
            self.bins = []

        return True


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    d = dict()

    for l, line in enumerate(text):
        print(f"line {l}: {line}")
        line = line.split()
        if line[0] == 'value':
            value = int(line[1])
            bot = ' '.join(line[-2:])
            print("adding ", bot)
            if not bot in d:
                d[bot] = Bot(bot, '', '', d)
            d[bot].add(value)

        elif line[0] == 'bot':
            bot = ' '.join(line[0:2])
            hi = ' '.join(line[-2:])
            lo = ' '.join(line[-7:-5])

            if hi not in d:
                d[hi] = Bot(hi, '', '', d)
            if lo not in d:
                d[lo] = Bot(lo, '', '', d)
            if bot not in d:
                d[bot] = Bot(bot, lo, hi, d)
            else:
                d[bot].lo = lo
                d[bot].hi = hi

    for k in d:
        if len(d[k].bins) >= 2:
            print(f"{k}: bins {len(d[k].bins)}")
            WAIT = False
            d[k].update()

    print(f"AOC {year} day {day}  Part One: {'one line up'}")

    ptwo = d['output 0'].bins[0] * d['output 1'].bins[0] * d['output 2'].bins[0]

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
