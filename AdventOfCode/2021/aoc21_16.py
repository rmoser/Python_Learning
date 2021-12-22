# Advent of Code
year = 2021
day = 16

import numpy as np
import aocd
import math
import logging

# logging.basicConfig(level=logging.DEBUG)

text0 = """
D2FE28
38006F45291200
EE00D40C823060
8A004A801A8002F478
620080001611562C8802118E34
C0015000016115A2E0802F182340
A0016C880162017C3686B18A3D4780
C200B40A82
04005AC33890
880086C3E88112
CE00C43D881120
D8005AC2A8F0
F600BC2D8F
9C005AC2F8F0
9C0141080250320F1802104A08
"""

text1 = aocd.get_data(day=day, year=year)

TABS = 0
TAB = '\t'


def hex2bin(s):
    d = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }

    return ''.join((d[c] for c in list(s)))


def parse_packet(packet, is_hex=False, packet_limit=None):
    global TABS, TAB
    TABS += 1

    if packet_limit is None:
        packet_limit = np.inf

    result = []

    if is_hex:
        bits = hex2bin(packet)
        logging.debug(f"{TAB*TABS}HEX-BITS: {packet} == {bits}")
    else:
        bits = packet

    while len(bits) > 10 and len(result) < packet_limit:
        logging.debug(f"{TAB*TABS}BITS: {bits}")
        v, bits = int(bits[:3], 2), bits[3:]
        t, bits = int(bits[:3], 2), bits[3:]

        logging.debug(f"{TAB*TABS}v: {v}, t: {t}")

        if t == 4:
            # literal value packet
            num, bits = value(bits)
            logging.debug(f"{TAB*TABS}Value packet: {num}")
            result.append((v, t, num))

        else:
            # operator packet
            i, bits = bits[0], bits[1:]
            logging.debug(f"{TAB*TABS}Oper packet: I={i}, {bits}")

            if i == '0':
                n, bits = int(bits[:15], 2), bits[15:]
                sub_packet, bits = bits[:n], bits[n:]
                logging.debug(f"{TAB*TABS}{n} bits: {sub_packet}")
                x, _ = parse_packet(sub_packet)
                result.append((v, t, x))

            else:
                n, bits = int(bits[:11], 2), bits[11:]

                logging.debug(f"{TAB*TABS}{n} packets: {bits}")
                x, bits = parse_packet(bits, packet_limit=n)
                result.append((v, t, x[:n]))

    TABS -= 1
    return result, bits


def value(s):
    result = ''
    while len(s) > 4:
        chunk, s = s[:5], s[5:]
        result += chunk[1:]
        if chunk[0] == '0':
            break
        # logging.debug((result, int(result, 2)))
    return int(result, 2), s


def sum_version(arr):
    if not hasattr(arr, '__iter__'):
        return 0
    if isinstance(arr, str):
        return 0

    total = 0
    for item in arr:
        if isinstance(item, tuple):
            total += item[0]
            total += sum_version(item[2])
            continue

        if isinstance(item, list):
            total += sum_version(item)

    return total


def score(arr):
    global TABS, TAB

    if isinstance(arr, str):
        return 0

    while True:
        logging.debug(f"{TAB * TABS} arr: {arr}")

        if isinstance(arr, int):
            return arr

        if isinstance(arr, list) and all(isinstance(x, int) for x in arr):
            if len(arr) == 1:
                return arr[0]
            else:
                return arr

        for i, chunk in enumerate(arr):
            if not isinstance(chunk, tuple):
                continue
            v, operation, operand = chunk
            if isinstance(operand, int) or all(isinstance(x, int) for x in operand):
                logging.debug(f"{TAB * TABS} {i}, {operation} -> {operand}")

                if operation == 4:
                    logging.debug(f"{TAB * TABS} STATIC: {operand}")
                    arr[i] = operand
                    continue

                logging.debug(f"{TAB * TABS} Recurse Operand: {operand}")
                TABS += 1
                operand = score(operand)
                logging.debug(f"{TAB * TABS} Recurse Got: {operand}")
                TABS -= 1
                if operation == 0:
                    logging.debug(f"{TAB * TABS} Sum: {operand}")
                    if isinstance(operand, int):
                        arr[i] = operand
                    else:
                        arr[i] = sum(operand)
                elif operation == 1:
                    logging.debug(f"{TAB * TABS} Prod: {operand}")
                    if isinstance(operand, int):
                        arr[i] = operand
                    else:
                        arr[i] = math.prod(operand)
                elif operation == 2:
                    logging.debug(f"{TAB * TABS} Min: {operand}")
                    if isinstance(operand, int):
                        arr[i] = operand
                    else:
                        arr[i] = min(operand)
                elif operation == 3:
                    logging.debug(f"{TAB * TABS} Max: {operand}")
                    if isinstance(operand, int):
                        arr[i] = operand
                    else:
                        arr[i] = max(operand)
                elif operation == 5:
                    logging.debug(f"{TAB * TABS} >: {operand}")
                    arr[i] = int(operand[0] > operand[1])
                elif operation == 6:
                    logging.debug(f"{TAB * TABS} <: {operand}")
                    arr[i] = int(operand[0] < operand[1])
                elif operation == 7:
                    logging.debug(f"{TAB * TABS} =: {operand}")
                    arr[i] = int(operand[0] == operand[1])

            else:
                logging.debug(f"{TAB * TABS} Recurse: {arr[i]}")
                TABS += 1
                arr[i] = (v, operation, score(operand))
                TABS -= 1


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    # text = text[8:9]

    d = dict()
    for packet in text:
        x, _ = parse_packet(packet, is_hex=True)
        d[packet] = x

    logging.debug("SUMMARY")
    total = 0
    for k, v in d.items():
        _score = sum_version(v)
        logging.debug((k, _score, v))
        total += _score

    pone = total
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = score(list(d.values())[0])
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
