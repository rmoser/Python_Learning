# Advent of Code
from fontTools.misc.bezierTools import lineLineIntersections

year = 2024
day = 24

import numpy as np
import aocd
import os
import itertools as it
from typing import Type
from pprint import pprint

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

text0 = """
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
"""

text1 = aocd.get_data(day=day, year=year)

class Node(object):
    nodes = dict()

    @classmethod
    def __is_node(cls, name: (str, type['Node'])):
        return isinstance(name, Node) or name in cls.nodes and isinstance(cls.nodes[name], Node)

    @classmethod
    def output_value(cls, n: str):
        return int(cls.output_value_binary(n), 2)

    @classmethod
    def output_value_binary(cls, n: str):
        return ''.join([str(cls.nodes[x].output) for x in
                            sorted([k for k in cls.nodes.keys() if k.startswith(n)], reverse=True)])

    @classmethod
    def as_node(cls, input: (str, 'Node')):
        if isinstance(input, str):
            return Node.nodes[input]
        return input

    @classmethod
    def traceback(cls, node: ('Node', str)):
        result = []
        stack = list(cls.as_node(node).inputs)

        while stack:
            n = stack.pop()
            if n in result:
                continue

            if isinstance(n, str) and n in Node.nodes:
                n = Node.nodes[n]

            if isinstance(n, Node):
                result.append(n)
                for x in n.inputs:
                    stack.append(cls.as_node(x))

        return result

    @classmethod
    def trace_gate(cls, num: int):
        result = dict()
        errors = []
        _num = f'{num:0>2}'
        _x0 = f'x{_num}'
        _y0 = f'y{_num}'
        _z0 = f'z{_num}'
        _c0 = f'c{_num}'
        # _z1 = f'z{num+1:0>2}'

        for c in (_z0, _y0, _x0):
            n = Node.nodes[c]
            result[c] = n

        # Logic gates
        # x0 XOR y0 -> a
        # x0 AND y0 -> b
        # c0 XOR a -> z0
        # c0 AND a -> d
        # d OR b -> c1

        a, d, b, cin, cout = None, None, None, None, None

        if num == 0:
            for _node in n.outputs:
                _node = cls.as_node(_node)
                if _node.inputs == {_x0, _y0}:
                    if _node.op == 'AND':
                        cout = _node
                        _node.label = f'c{_num}'

                    elif _node.op == 'XOR':
                        z0 = _node
                        _node.label = _z0


        else:
            for _node in n.outputs:
                _node = cls.as_node(_node)
                if _node.inputs == {_x0, _y0}:
                    if _node.op == 'AND':
                        b = _node
                        _node.label = f'b{_num}'

                    elif _node.op == 'XOR':
                        a = _node
                        _node.label = f'a{_num}'
            if not a:
                errors.append(['Missing A'])
            if not b:
                errors.append(['Missing B'])

            for _node in a.outputs:
                _node = cls.as_node(_node)
                if _node.op == 'XOR':
                    z0 = _node
                    _node.label = _z0
                elif _node.op == 'AND':
                    d = _node
                    _node.label = f'd{_num}'

            for _node in b.outputs:
                _node = cls.as_node(_node)
                if _node.op == 'OR':
                    cout = _node
                    _node.label = f'c{_num}'

            for n in z0.inputs:
                if n != a.name:
                    cin = cls.as_node(n)

            if not d:
                errors.append(['Missing D'])

        if not z0:
            errors.append([f'Missing {_z0}'])
        if not cout:
            errors.append([f'Missing {_c0}'])

        result['a'] = a
        result['b'] = b
        result['d'] = d
        result['cin'] = cin
        result['cout'] = cout

        # Check wiring for errors
        if num:
            if a.inputs != {_x0, _y0} or a.op != 'XOR':
                errors.append(['a', a])
            if b.inputs != {_x0, _y0} or b.op != 'AND':
                errors.append(['b', b])
            if d.inputs != {a.name, cin.name}:
                errors.append(['d', d])
            if cin.outputs != {z0.name, d.name}:
                errors.append(['c0', cin])
            if cout.inputs != {d.name, b.name}:
                errors.append(['c1', cout])
        else:
            if z0.inputs != {_x0, _y0}:
                errors.append([_z0])
            if cout.inputs != {_x0, _y0}:
                errors.append([_c0, cout])

        if z0.name != _z0:
            errors.append([_z0, z0.name])
        if Node.as_node(_x0).outputs != Node.as_node(_y0).outputs:
            errors.append([_x0, "outputs !=", _y0])

        return errors, result

    @classmethod
    def traceforward(cls, node):
        result = []
        stack = list(cls.as_node(node).outputs)

        while stack:
            n = cls.as_node(stack.pop())
            if n in result:
                continue

            result.append(n)
            # print(f'{n.name} -> [{n.outputs}]')
            for x in n.outputs:
                if x:
                    stack.append(cls.as_node(x))

        return result


    @classmethod
    def parse_loop(cls):
        not_ready = [x for x in cls.nodes.values() if not x.ready]
        while not_ready:
            x = not_ready.pop(0)
            x.parse()
            if not x.ready:
                not_ready.append(x)

    @classmethod
    def calc_loop(cls):
        not_done = [x for x in cls.nodes.values() if not x.done]
        while not_done:
            x = not_done.pop(0)
            x.calc()
            if not x.done:
                not_done.append(x)


    def __init__(self, name: str, value: (str, int)):
        self.name = name
        self.label = ''
        if name[0] in 'xy':
            self.label = name
        self.output = value
        self.nodes[name] = self

        self.outputs = set()
        self.inputs = set()
        self.op = ''
        self.ready = False
        self.done = False
        self.parse()

    def __repr__(self):
        if len(self.inputs) == 2:
            return f'Node {self.name}/{self.label}: {f" {self.op} ".join(self.inputs)} = {self.output}.'
        return f'Node {self.name}: {self.output}'

    def __str__(self):
        return f'Node {self.name}'

    def parse(self):
        if not self.ready:
            if isinstance(self.output, str):
                if len(self.output) == 1:
                    self.output = int(self.output)
                    self.ready = True
                    self.done = True
                else:
                    a, self.op, b = self.output.split()
                    self.inputs = {a, b}
                    if self.__is_node(a):
                        a = self.nodes[a]
                        a.outputs.add(self.name)
                        if not a.ready:
                            a.parse()
                    if self.__is_node(b):
                        b = self.nodes[b]
                        b.outputs.add(self.name)
                        if not b.ready:
                            b.parse()

        if self.inputs and all(self.__is_node(n) and self.nodes[n].ready for n in self.inputs):
            self.ready = True

        if self.ready:
            self.calc()

    def calc(self):
        if self.ready and len(self.inputs) == 2:
            a, b = (self.nodes[x] for x in self.inputs)
            if a.done and b.done:
                a = a.output
                b = b.output
                match self.op:
                    case 'AND':
                        self.output = int(a & b)
                    case 'OR':
                        self.output = int(a | b)
                    case 'XOR':
                        self.output = int(a ^ b)

                self.done = True

    def recalc_outputs(self):
        self.calc()
        for n in self.outputs:
            self.nodes[n].recalc_outputs()

    def rewire(self, other):
        other = self.nodes[other]

        self.inputs, other.inputs = other.inputs, self.inputs
        self.op, other.op = other.op, self.op

        for node in self.inputs | other.inputs:
            node = self.as_node(node)
            if self.name in node.outputs and other.name not in node.outputs:
                node.outputs = node.outputs - {self.name} | {other.name}
            elif self.name not in node.outputs and other.name in node.outputs:
                node.outputs = node.outputs - {other.name} | {self.name}

        for node in self.outputs | other.outputs:
            node = self.as_node(node)
            if self.name in node.inputs and other.name not in node.inputs:
                node.inputs = node.inputs - {self.name} | {other.name}
            elif self.name not in node.inputs and other.name in node.inputs:
                node.inputs = node.inputs - {other.name} | {self.name}

        self.calc()
        other.calc()
        for x in self.outputs | other.outputs:
            self.nodes[x].calc()

    def get_op(self, op, forward=True):
        result = []
        _nodes = self.outputs if forward else self.inputs
        for n in _nodes:
            node = self.nodes[n]
            if node.op == op:
                result.append(node)
        return result

def run(system: dict):
    bits = ('0', '1')
    z_keys = list(reversed(sorted([k for k in system.keys() if k.startswith('z')])))

    def done():
        return all(len(system[k]) == 1 for k in z_keys)

    while not done():
        for k, v in system.items():
            if len(v) == 1:
                continue

            a, op, b = v

            _a = system[a]
            _b = system[b]
            if len(_a) == 1 and len(_b) == 1:
                match op:
                    case 'AND':
                        system[k] = bits[_a=='1' and _b=='1']
                    case 'OR':
                        system[k] = bits[_a=='1' or _b=='1']
                    case 'XOR':
                        system[k] = bits[(_a=='1') ^ (_b=='1')]



def check():
    x1 = Node.output_value('x')
    y1 = Node.output_value('y')
    z1 = Node.output_value('z')

    pone = z1

    ans = x1 + y1

    delta = f'{z1 ^ (x1+y1):b}'

    bad_outputs = np.where(np.array(list(reversed(delta)), dtype=int))[0]
    bad_output_names = [x for x in [f'z{i:0>2}' for i in bad_outputs] if x in Node.nodes and x[0] not in ('x', 'y')]

    if not bad_output_names:
        return True, []
    else:
        return False, bad_output_names


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    errors = []

    nodes = []

    for line in text:
        if not line:
            continue

        if ': ' in line:
            a, b = line.split(': ')
        else:
            b, a = line.split(' -> ')
            for x in errors:
                if a in x:
                    i = x.index(a)
                    a = x[1-i]
                break

        nodes.append(Node(a, b))

    Node.parse_loop()
    Node.calc_loop()

    pone = Node.output_value('z')

    for i in range(sum(1 for x in Node.nodes.keys() if x.startswith('x'))):
        e, r = Node.trace_gate(i)
        if e:
            break

    print(i)
    pprint(e)
    pprint(r)

    # suspect_nodes = list(it.chain(*[Node.connected(x) for x in bad_output_names]))

    # Node.nodes['z05'].rewire('z00')
    # Node.nodes['z01'].rewire('z02')

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
