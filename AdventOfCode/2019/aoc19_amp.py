import numpy as np
from queue import Queue
from icecream import ic

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

            ic('i:', self.i, inst, self.arr[self.i:self.i+5], self.arr[self.i], self.op)

            match self.op:
                case 1:
                    a, b, c = self.arr[self.i+1:self.i+4]
                    ic(f'\tA {a_mode}: {a}')
                    ic(f'\tB {b_mode}: {b}')
                    ic(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    ic(f'op {self.op}: Add {a} + {b} => {c}')

                    self.arr[c] = a + b
                    self.i += 4

                case 2:
                    a, b, c = self.arr[self.i+1:self.i+4]
                    ic(f'\tA {a_mode}: {a}')
                    ic(f'\tB {b_mode}: {b}')
                    ic(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    ic(f'op {self.op}: Mul {a} * {b} => {c}')

                    self.arr[c] = a * b
                    self.i += 4

                case 3:  # Input
                    if self.input_value.empty():
                        raise IndexError(f"Out of input values.")

                    a = self.arr[self.i+1]
                    ic(f'\tA {a_mode}: {a}')

                    if a_mode:
                        raise ReferenceError(f"Invalid a_mode: {a_mode} in {inst}")
                    ic(f'op {self.op}: Stor {input_values} => {a}')

                    self.arr[a] = self.input_value.get()
                    self.i += 2

                case 4:  # Output
                    a = self.arr[self.i+1]
                    ic(f'\tA {a_mode}: {a}')
                    ic(f'op {self.op}: Output {a}')
                    a = a if a_mode else self.arr[a]
                    self.i += 2
                    return a

                case 5:  # Jmp If True
                    a, b = self.arr[self.i+1:self.i+3]
                    ic(f'\tA {a_mode}: {a}')
                    ic(f'\tB {b_mode}: {b}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    ic(f'op {self.op}: JMP True: {a} => {b}')
                    if a != 0:
                        self.i = b
                    else:
                        self.i += 3

                case 6:  # Jmp if False
                    a, b = self.arr[self.i+1:self.i+3]
                    ic(f'\tA {a_mode}: {a}')
                    ic(f'\tB {b_mode}: {b}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    ic(f'op {self.op}: JMP False: {a} => {b}')
                    if a == 0:
                        self.i = b
                    else:
                        self.i += 3
                    pass

                case 7:  # Less Than
                    a, b, c = self.arr[self.i+1:self.i+4]
                    ic(f'\tA {a_mode}: {a}')
                    ic(f'\tB {b_mode}: {b}')
                    ic(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    ic(f'op {self.op}: LT: {a} < {b}')
                    self.arr[c] = int(a < b)
                    self.i += 4

                case 8:  # Equals
                    a, b, c = self.arr[self.i+1:self.i+4]
                    ic(f'\tA {a_mode}: {a}')
                    ic(f'\tB {b_mode}: {b}')
                    ic(f'\tC {c_mode}: {c}')

                    a = a if a_mode else self.arr[a]
                    b = b if b_mode else self.arr[b]
                    ic(f'op {self.op}: EQ: {a} == {b}')
                    self.arr[c] = int(a == b)
                    self.i += 4

                case 99:
                    break

                case _:
                    raise IndexError(f"Invalid opcode {self.op}")

