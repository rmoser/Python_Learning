# Advent of Code
year = 2019
day = 5

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)


def intcode(arr):
    i = 0
    while True:
        inst = str(arr[i]).rjust(5, '0')
        op = int(inst[-2:])
        c_mode, b_mode, a_mode = (int(x) for x in op[:3])

        # print(i, arr[i], arr)
        if a_mode:
            a = arr[i+1]
        else:
            a = arr[arr[i + 1]]

        if b_mode:
            b = arr[i+2]
        else:
            b = arr[arr[i + 2]]

        if c_mode:
            c = arr[i+3]
        else:
            c = arr[arr[i + 3]]

        match op:
            case '01':
                arr[c] = a + b
                i += 4

            case '02':
                arr[c] = a * b
                i += 4

            case '03':
                arr[]
                pass

            case '04':
                pass

            case '99':
                break


    # print(arr)
    return arr[0]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
