# Advent of Code
import itertools

year = 2022
day = 15

import numpy as np
import aocd
import itertools

text0 = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
text1 = aocd.get_data(day=day, year=year)


def perimeter(sensor, beacon, rng=None):
    d = np.abs(np.array(sensor) - beacon).sum() + 1
    for i in range(d):
        new = {(sensor[0] + i, sensor[1] + d - i), (sensor[0] + d - i, sensor[1] - i),
             (sensor[0] - i, sensor[1] - d + i), (sensor[0] - d + i, sensor[1] + i)}
        if rng:
            for coord in new.copy():
                if coord[0] < rng[0] or coord[1] > rng[1]:
                    new.remove(coord)
                    continue
        yield new


def check_all(sensors, beacons, distances, rng):
    for i in range(len(sensors)):
        for cset in perimeter(sensors[i], beacons[i], rng=rng):
            for c in cset:
                if check(c, sensors, beacons, distances, rng):
                    return c


def check(coord, sensors, beacons, distances, rng):
    coord = np.array(coord)
    if (coord < rng[0]).any() or (coord > rng[1]).any():
        return False
    d = np.abs(np.array(sensors) - coord).sum(axis=1)
    return (d > np.array(distances)).all()


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    if text == text0:
        y = 10
        ymax = 20
        rng = (0, 20)
    else:
        y = 2_000_000
        ymax = 4_000_000
        rng = (0, 4_000_000)

    text = text.strip().splitlines()

    for i, line in enumerate(text):
        sensor, beacon = line.split(": ")
        sensor = tuple(int(x) for x in sensor[12:].split(', y='))
        beacon = tuple(int(x) for x in beacon[23:].split(', y='))
        text[i] = sensor, beacon

    data = np.array(text)
    xmin = data[:, :, 0].min()
    xmax = data[:, :, 0].max()
    ymin = data[:, :, 1].min()
    ymax = data[:, :, 1].max()

    sensors = data[:, 0, :]
    beacons = data[:, 1, :]
    distances = np.abs(sensors - beacons).sum(axis=1)
    offset = distances.end()

    # x_values = set()

    arr = np.zeros(dtype=bool, shape=(len(sensors), xmax - xmin + 1 + offset * 2))

    sensors = [tuple(sensors[i]) for i in range(len(sensors))]
    beacons = [tuple(beacons[i]) for i in range(len(beacons))]

    for i in range(len(sensors)):
        s = sensors[i]
        b = beacons[i]
        d = distances[i]

        y_delta = np.abs(y - s[1])

        if y_delta > d:
            continue

        arr[i, s[0] - d + y_delta + offset: s[0] + d - y_delta + 1 + offset] = True

    x_values = set(np.where(arr.any(axis=0))[0] - offset)

    coords = set(sensors) | set(beacons)

    for coord in coords:
        if coord[1] == y and coord[0] in x_values:
            x_values.remove(coord[0])

    pone = len(x_values)

    print(f"AOC {year} day {day}  Part One: {pone}")

    # PTWO
    # perimeters = list(range(len(sensors)))
    # for i in range(len(sensors)):
    #     perimeters[i] = set(perimeter(sensors[i], beacons[i], rng=rng))
    #
    # coords = set()
    # for a, b, c, d in itertools.combinations(perimeters, 4):
    #     i = a & b & c & d
    #     if i:
    #         coords |= i
    #         print(coords)
    #
    # for coord in coords:
    #     if (np.abs(np.array(sensors) - coord).sum() > np.array(distances).reshape((len(sensors), 1))).all():
    #         x = coord[0]
    #         y = coord[1]

    x, y = check_all(sensors, beacons, distances, rng)
    print(x, y)
    ptwo = np.int64(x) * 4000000 + y

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
