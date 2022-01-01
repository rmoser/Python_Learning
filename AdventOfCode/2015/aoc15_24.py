# Advent of Code
year = 2015
day = 24

import numpy as np
import aocd
import itertools

text0 = """
1 2 3 4 5 7 8 9 10 11
""".replace(' ', '\n')

text1 = aocd.get_data(day=day, year=year)


def find_bundles(values, total, size=None, count=None):
    if count is None:
        count = np.inf

    v = np.array(list(values))
    i = v.argsort()
    v = v[i[::-1]]

    csum = v.cumsum()
    if (csum == total).any():
        return [np.extract(csum <= total, v)]

    if size is None:
        min_count = (csum <= total).sum() + 1
        max_count = len(v) // 2 + 2
    else:
        min_count = size
        max_count = size + 1

    bundles = []

    # Bounds for bag size to capture half the total 'weight'
    for size in range(min_count, max_count):
        for bag in itertools.combinations(v, r=size):
            bag = np.array(bag)

            if bag.sum() == total:
                bundles.append(bag)

                if count and len(bundles) >= count:
                    return bundles

    return bundles


def find_n_bundles(values, weight=None, groups=1):
    v = np.array(list(values))

    if weight is None or weight <= 0:
        weight = v.sum() // groups

    # Single bag check
    if groups == 1:
        if v.sum() == weight:
            return [values]
        else:
            return []

    bag = find_bundles(v, weight, count=1)[0]

    size = len(bag)

    for s in range(size, len(v) // 2 + 2):
        # print("Searching for bundles of size: ", s)
        bags = find_bundles(values, weight, size=s)

        # print(f"Found {len(bags)} bundles of size {s}")
        for b in bags:
            rest = set(values) - set(b)
            other_bags = find_n_bundles(rest, weight, groups-1)
            if len(other_bags) == groups-1:
                # print([b] + other_bags)
                return [b] + other_bags

    return []


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    arr = np.array(text).astype(int)[::-1]
    # arr = np.atleast_2d(arr)


    groups = 3
    weight = arr.sum() // groups

    # values = arr.flatten()[::-1]
    #
    # bag_one = np.extract(values.cumsum() < weight, values)

    values = arr

    bag = find_bundles(values, weight, count=1)[0]

    size = len(bag)

    bundles = []
    for s in range(size, len(values) // 2 + 2):
        print("Searching for bundles of size: ", s)
        bags = find_bundles(values, weight, size=s)

        print(f"Found {len(bags)} bundles of size {s}")
        for b in bags:
            rest = set(values) - set(b)

            other_bags = find_n_bundles(rest, weight=weight, groups=groups-1)

            if len(other_bags) == groups - 1:
                bundles.append([b] + other_bags)
                print(f"Found {len(bundles)} valid bundles of size {s}")

        if len(bundles):
            break

    qe = np.array([bundle[0].astype(np.int64) for bundle in bundles]).prod(axis=1)

    pone = qe.min()

    print(f"AOC {year} day {day}  Part One: {pone}")


    groups = 4
    weight = arr.sum() // groups

    # values = arr.flatten()[::-1]
    #
    # bag_one = np.extract(values.cumsum() < weight, values)

    values = arr

    bag = find_bundles(values, weight, count=1)[0]

    size = len(bag)

    bundles = []
    for s in range(size, len(values) // 2 + 2):
        print("Searching for bundles of size: ", s)
        bags = find_bundles(values, weight, size=s)

        print(f"Found {len(bags)} bundles of size {s}")
        for b in bags:
            rest = set(values) - set(b)

            other_bags = find_n_bundles(rest, weight=weight, groups=groups-1)

            if len(other_bags) == groups - 1:
                bundles.append([b] + other_bags)
                print(f"Found {len(bundles)} valid bundles of size {s}")

        if len(bundles):
            break

    qe = np.array([bundle[0].astype(np.int64) for bundle in bundles]).prod(axis=1)

    ptwo = qe.min()

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
