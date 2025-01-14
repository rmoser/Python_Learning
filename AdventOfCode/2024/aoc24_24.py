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
        _num = f'{num:0>2}'
        _x0 = f'x{_num}'
        _y0 = f'y{_num}'
        _z0 = f'z{_num}'
        _c0 = f'c{_num}'
        _c_1 = f'c{num-1:0>2}'
        # _z1 = f'z{num+1:0>2}'

        for c in (_z0, _y0, _x0):
            n = Node.nodes[c]
            result[c.upper()] = n

        # Logic gates
        # x0 XOR y0 -> a
        # x0 AND y0 -> b
        # c0 XOR a -> z0
        # c0 AND a -> d
        # d OR b -> c1

        seen_nodes = set(result.values())
        a, d, b, cin, cout, z0 = None, None, None, None, None, None

        if num == 0:
            for _node in n.outputs:
                _node = cls.as_node(_node)
                seen_nodes.add(_node)
                if _node.inputs == {_x0, _y0}:
                    if _node.op == 'AND':
                        cout = _node
                        _node.label = f'c{_num}'

                    elif _node.op == 'XOR':
                        z0 = _node
                        _node.label = _z0
                    else:
                        seen_nodes.add(_node)

        else:
            for _node in n.outputs:
                _node = cls.as_node(_node)
                seen_nodes.add(_node)
                if _node.inputs == {_x0, _y0}:
                    if _node.op == 'AND':
                        b = _node
                        _node.label = f'b{_num}'

                    elif _node.op == 'XOR':
                        a = _node
                        _node.label = f'a{_num}'

            for _node in a.outputs if a else set():
                _node = cls.as_node(_node)
                seen_nodes.add(_node)
                if _node.op == 'XOR':
                    z0 = _node
                    _node.label = _z0

            if not z0 and Node.nodes[_z0].op == 'XOR':
                z0 = Node.nodes[_z0]
                seen_nodes.add(z0)
                z0.label = _z0

            for _node in (a.outputs if a else set()):
                _node = cls.as_node(_node)
                seen_nodes.add(_node)
                if _node.op == 'AND':
                    d = _node
                    _node.label = f'd{_num}'

            for _node in cls.nodes.values():
                if _node.label == _c_1:
                    cin = _node
                    seen_nodes.add(cin)

            if not cin:
                for _node in (z0.inputs if z0 else set() | (d.inputs if d else set())):
                    if _node != a.name:
                        cin = cls.as_node(_node)
                        seen_nodes.add(cin)

            for _node in (b.outputs if b else set()) | (d.outputs if d else set()):
                _node = cls.as_node(_node)
                seen_nodes.add(_node)
                if _node.op == 'OR':
                    cout = _node
                    _node.label = f'c{_num}'

        result['a'] = a
        result['b'] = b
        result['d'] = d
        result['cin'] = cin
        result['cout'] = cout
        result[_z0] = z0
        result['unk'] = {n for n in seen_nodes if not n.label}

        # Check wiring for errors
        _errors = []
        if num:
            if not a or a.inputs != {_x0, _y0} or a.op != 'XOR' or len(a.outputs) != 2:
                if a:
                    _errors.append(a.name)
            if not b or b.inputs != {_x0, _y0} or b.op != 'AND' or len(b.outputs) != 1:
                if b:
                    _errors.append(b.name)
            if not d or d.inputs != {a.name, cin.name} or d.op != 'AND' or len(d.outputs) != 1:
                if d:
                    _errors.append(d.name)
            if not cin or cin.op != ('OR' if num > 1 else 'AND') or len(cin.outputs) != 2:
                if cin:
                    _errors.append(cin.name)
            if not cout or cout.op != 'OR' or len(cout.inputs) != 2:
                if cout:
                    _errors.append(cout.name)
            if not z0 or z0.name != _z0 or z0.op != 'XOR' or len(z0.inputs) != 2 or len(z0.outputs) != 0:
                if z0 and z0.name not in _errors:
                    _errors.append(z0.name)
                if _z0 not in _errors:
                    _errors.append(_z0)
        else:
            if not z0 or z0.inputs != {_x0, _y0} or z0.op != 'XOR':
                _errors.append(z0.name if z0 else _z0)
            if not cout or cout.inputs != {_x0, _y0} or cout.op != 'AND':
                _errors.append(cout.name if cout else _c0)

        # if Node.as_node(_x0).outputs != Node.as_node(_y0).outputs:
        #     _errors.append([_x0, "outputs !=", _y0])

        _suspect_nodes = {n.name for n in seen_nodes if not n.label and n.op}
        if _suspect_nodes and len(_suspect_nodes) % 2 == 0:
            _errors += list(_suspect_nodes)
        return _errors, result

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
            return f'Node {self.name}/{self.label}: {f" {self.op} ".join(self.inputs)} = {self.output} -> {self.outputs}.'
        return f'Node {self.name}: {self.output} -> {self.outputs}.'

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
        self.label, other.label = other.label, self.label

        for node in self.inputs | other.inputs:
            node = self.as_node(node)
            node.outputs = {k for k, v in Node.nodes.items() if node.name in v.inputs}

        self.outputs = {k for k, v in Node.nodes.items() if self.name in v.inputs}
        other.outputs = {k for k, v in Node.nodes.items() if other.name in v.inputs}

        self.calc()
        other.calc()
        self.nodes['x00'].recalc_outputs()
        # self.recalc_outputs()
        # other.recalc_outputs()

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

    print(f'{x1} + {y1} = {x1+y1}')
    print(f'Adder result: {z1}')

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
                    num = x.index(a)
                    a = x[1 - num]
                break

        nodes.append(Node(a, b))

    Node.parse_loop()
    Node.calc_loop()

    pone = Node.output_value('z')

    traces = dict()
    for num in range(sum(1 for x in Node.nodes.keys() if x.startswith('x'))):
        e, r = Node.trace_gate(num)
        traces[num] = r
        if e:
            while len(e) and (len(e) % 2) == 0:
                e = tuple(e)
                Node.nodes[e[0]].rewire(e[1])
                errors.append(e[:2])
                e, r = Node.trace_gate(num)

    ptwo = ','.join(sorted(it.chain(*errors)))
    # suspect_nodes = list(it.chain(*[Node.connected(x) for x in bad_output_names]))

    # Node.nodes['z05'].rewire('z00')
    # Node.nodes['z01'].rewire('z02')

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
