# Advent of Code
year = 2020
day = 13

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import math

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
939
7,13,x,x,59,x,31,19
"""

text0 = ("0\n1789,37,47,1889")

text1 = aocd.get_data(day=day, year=year)

def next_bus(now, bus):
    return math.ceil(now / bus) * bus

def get_offset(bus_0, bus_1):
    if bus_0[1] > bus_1[1]:
        bus_0, bus_1 = bus_1, bus_0
    bus_a, offset_a = bus_0
    bus_b, offset_b = bus_1
    _offset_a = offset_a % bus_a
    _offset_b = offset_b % bus_b

    step = bus_a
    time = step

    departure_delay = offset_b - offset_a
    while next_bus(time-_offset_a, bus_b) - time != _offset_b - _offset_a:
        # print(time-offset_a)
        time += step

    # print(f"Period: {step}, Time {time-offset_a} for bus {bus}")
    return time-_offset_a


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    start = int(text[0])
    data = text[1].split(',')

    buses = dict()
    for bus in data:
        if not bus.isnumeric():
            continue
        bus = int(bus)
        buses[bus] = next_bus(start, bus)

    next_departure = min(buses.values())
    bus = max(b for b in buses if buses[b] == next_departure)

    pone = bus * (next_departure - start)
    print(f"AOC {year} day {day}  Part One: {pone}")

    data = {int(x): i for i, x in enumerate(data) if x.isnumeric()}
    # _data = sorted(data.keys(), reverse=True)
    _data = sorted(data.keys())

    bus = _data[0]
    bus = (bus, data[bus])
    for i in range(1, len(_data)):
        _bus = (_data[i], data[_data[i]])
        new_bus = (bus[0] * _bus[0], -1 * get_offset(bus, _bus))
        # print(f'{i}: {bus} + {_bus} -> {new_bus}')
        bus = new_bus

    # pprint(data)
    # b = 1
    # step = _data[0]
    # offset = 0
    # multipliers = [1]
    # time = step
    # while True:
    #     bus = _data[b]
    #     departure_delay = data[bus]
    #     print(f"Period: {step}, Time {time} for bus {bus} {b+1}/{len(data)}")
    #     while next_bus(time, bus) - time != departure_delay:
    #         time += step
    #
    #     step *= bus
    #     offset = time
    #     b += 1
    #
    #     if b >= len(data):
    #         break

    ptwo = -bus[1]

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
