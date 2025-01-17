# Advent of Code
year = 2020
day = 4

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import re

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
text1 = aocd.get_data(day=day, year=year)

REQUIRED = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')  #, 'cid')

def valid(passport):
    return all(x in passport for x in REQUIRED)

def valid2(passport):
    if not 'byr' in passport or not (1920 <= int(passport['byr']) <= 2002):
        return False
    if not 'iyr' in passport or not (2010 <= int(passport['iyr']) <= 2020):
        return False
    if not 'eyr' in passport or not (2020 <= int(passport['eyr']) <= 2030):
        return False
    if not 'hgt' in passport:
        return False
    if passport['hgt'][-2:] not in ('in', 'cm'):
        return False
    h = int(passport['hgt'][:-2])
    if passport['hgt'].endswith('in') and not 59 <= h <= 76:
        return False
    if passport['hgt'].endswith('cm') and not 150 <= h <= 193:
        return False

    if not 'hcl' in passport or not re.fullmatch(r'^#[\dabcdef]{6}', passport['hcl']):
        return False
    if not 'ecl' in passport or not passport['ecl'] in ('amb','blu','brn','gry','grn','hzl','oth'):
        return False
    if not 'pid' in passport or not re.fullmatch(r'[\d]{9}', passport['pid']):  # Add regex
        return False

    return True


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n')


    passports = list()
    for line in text:
        d = dict()
        for field in line.split():
            name, value = field.split(':')
            d[name] = value
        passports.append(d)

    pone = sum(valid(passport) for passport in passports)

    ptwo = sum(valid2(passport) for passport in passports)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
