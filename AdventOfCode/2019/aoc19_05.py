# Advent of Code
year = 2019
day = 5

import numpy as np
import aocd
from queue import Queue

#text0 = """3,225,1,225,6,6,1100,1,238,225,104,0,1102,45,16,225,2,65,191,224,1001,224,-3172,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,90,55,225,101,77,143,224,101,-127,224,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1102,52,6,225,1101,65,90,225,1102,75,58,225,1102,53,17,224,1001,224,-901,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,1002,69,79,224,1001,224,-5135,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,102,48,40,224,1001,224,-2640,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,1101,50,22,225,1001,218,29,224,101,-119,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,48,19,224,1001,224,-67,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1101,61,77,225,1,13,74,224,1001,224,-103,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,1102,28,90,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,7,226,677,224,102,2,223,223,1005,224,329,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,359,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,389,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,404,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,419,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,434,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,449,101,1,223,223,7,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,108,677,226,224,102,2,223,223,1005,224,479,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,494,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,509,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,524,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,539,1001,223,1,223,8,677,226,224,102,2,223,223,1005,224,554,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,569,1001,223,1,223,107,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,599,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,614,1001,223,1,223,1108,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,677,677,224,102,2,223,223,1005,224,644,1001,223,1,223,1008,677,677,224,102,2,223,223,1005,224,659,101,1,223,223,1107,677,226,224,1002,223,2,223,1006,224,674,101,1,223,223,4,223,99,226"""
text0 = """3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""
text1 = aocd.get_data(day=day, year=year)

class Amp:
    def __init__(self, id, arr_init, debug=False):
        self.id = id
        self.i = 0
        self.op = None
        self.input_value = Queue()
        self.arr = arr_init.copy()
        self.debug = debug

    def add(self, input_value):
        self.input_value.put(input_value)

    def run(self, input_values: int | list[int] | tuple[int] | np.ndarray[int] | None = None):
        if not np.iterable(input_values):
            if input_values is not None:
                self.input_value.put(input_values)
        else:
            for item in input_values:
                self.input_value.put(item)

        while True:
            inst = str(self.arr[self.i]).rjust(5, '0')
            self.op = int(inst[-2:])  # opcode
            c_mode, b_mode, a_mode = (int(x) for x in inst[:3])

            if self.debug:
                print('i:', self.i, inst, self.arr[self.i:self.i+5], self.arr[self.i], self.op)

            match self.op:
                case 1:
                    a, b, c = self.arr[self.i+1:self.i+4]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')
                        print(f'\tB {b_mode}: {b}')
                        print(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    if self.debug:
                        print(f'op {self.op}: Add {a} + {b} => {c}')
                    self.arr[c] = a + b
                    self.i += 4

                case 2:
                    a, b, c = self.arr[self.i+1:self.i+4]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')
                        print(f'\tB {b_mode}: {b}')
                        print(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    if self.debug:
                        print(f'op {self.op}: Mul {a} * {b} => {c}')
                    self.arr[c] = a * b
                    self.i += 4

                case 3:  # Input
                    if self.input_value.empty():
                        raise IndexError(f"Out of input values.")

                    a = self.arr[self.i+1]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')

                    if a_mode:
                        raise ReferenceError(f"Invalid a_mode: {a_mode} in {inst}")
                    if self.debug:
                        print(f'op {self.op}: Stor {input_values} => {a}')
                    self.arr[a] = self.input_value.get()
                    self.i += 2

                case 4:  # Output
                    a = self.arr[self.i+1]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')
                        print(f'op {self.op}: Output {a}')
                    a = a if a_mode else self.arr[a]
                    self.i += 2
                    return a

                case 5:  # Jmp If True
                    a, b = self.arr[self.i+1:self.i+3]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')
                        print(f'\tB {b_mode}: {b}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    if self.debug:
                        print(f'op {self.op}: JMP True: {a} => {b}')
                    if a != 0:
                        self.i = b
                    else:
                        self.i += 3

                case 6:  # Jmp if False
                    a, b = self.arr[self.i+1:self.i+3]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')
                        print(f'\tB {b_mode}: {b}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    if self.debug:
                        print(f'op {self.op}: JMP False: {a} => {b}')
                    if a == 0:
                        self.i = b
                    else:
                        self.i += 3
                    pass

                case 7:  # Less Than
                    a, b, c = self.arr[self.i+1:self.i+4]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')
                        print(f'\tB {b_mode}: {b}')
                        print(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    if self.debug:
                        print(f'op {self.op}: LT: {a} < {b}')
                    self.arr[c] = int(a < b)
                    self.i += 4

                case 8:  # Equals
                    a, b, c = self.arr[self.i+1:self.i+4]
                    if self.debug:
                        print(f'\tA {a_mode}: {a}')
                        print(f'\tB {b_mode}: {b}')
                        print(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    if self.debug:
                        print(f'op {self.op}: EQ: {a} == {b}')
                    self.arr[c] = int(a == b)
                    self.i += 4

                case 99:
                    break

                case _:
                    raise IndexError(f"Invalid opcode {self.op}")


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    arr_init = [int(x) for x in text.split(',')]

    amp = Amp("p1", arr_init)
    while not pone:
        pone = amp.run(1)
    print(f"\nAOC {year} day {day}  Part One: {pone}")


    amp = Amp("p2", arr_init)
    ptwo = amp.run(5)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
