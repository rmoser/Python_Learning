# Advent of Code
year = 2019
day = 7

import numpy as np
import aocd
import itertools
from aoc19_05 import Amp

text0 = """3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"""
text1 = aocd.get_data(day=day, year=year)

def p1(arr_init):
    res = 0
    phase = None
    for phase_values in itertools.permutations(range(5)):
        amps = [Amp(ph, arr_init, debug=True) for ph in phase_values]
        val = 0
        for i, phase_value in enumerate(phase_values):
            val = amps[i].run((phase_value, val))
            print(phase_value, val)
            #val = val[-1]
        if val > res:
            res = val
            phase = phase_values
    return res, phase


def p2(phase_value, arr_init):
    num_values = len(phase_value)
    values = [0] * num_values
    amps = [Amp(f'{c}{ph}', arr_init, debug=True) for c, ph in zip('ABCDE', phase_value)]

    # First pass
    for ph, amp in zip(phase_value, amps):
        amp.add(ph)  # Runs until next input
    amps[0].add(0)

    _i = 0
    v = 0
    while True:
        for i in range(5):
            out = amps[i].run()
            if out is not None:
                v = out
            print(f"{_i}:  Amp {amps[i].id} values={values} idx: {amps[i].i} arr: {amps[i].arr} in:{list(amps[i].input_value.queue)}")

        if amps[4].op == 99:
            return v, phase_value

    return values, amps




if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    arr_init = [int(x) for x in text.split(',')]

    pone, phase = p1(arr_init)
    print(f"\n\nAOC {year} day {day}  Part One: {pone}\n\n")

    ptwo = p2([9,8,7,6,5], arr_init)
    print(f"\n\nAOC {year} day {day}  Part Two: {ptwo}")
