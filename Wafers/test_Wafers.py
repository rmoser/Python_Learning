import pytest
import Wafers
import math
import numpy as np
import copy


@pytest.mark.parametrize("value", [0, 0., "0", Wafers.Wafer('', 0)])
def test_typeddict_0(value):
    d = Wafers.TypedDict()
    assert len(d) == 0, "TypedDict should init empty"
    assert d._type is object, "TypedDict should allow any object type before data is inserted"
    d['a'] = value
    assert d._type is type(value)
    assert len(d) == 1

    if d._type is not object:
        try:
            d['x'] = object
        except TypeError:
            pass
        else:
            assert False, 'TypedDict should reject items of the wrong type'


def test_typeddict_1():
    d0 = {'a': 0, 'b': 1}

    # Init with existing dict data
    d = Wafers.TypedDict(dict=d0, required_type=int)

    assert len(d) == 2
    assert sorted(list(d.keys())) == ['a', 'b']
    assert 'a' in d
    assert 'b' in d
    assert 'c' not in d


def test_typeddict_2():
    d = Wafers.TypedDict(required_type=int)

    assert len(d) == 0

    d['a'] = 1
    assert len(d) == 1
    assert list(d.keys()) == ['a']
    assert 'a' in d
    assert 1 in d
    assert 2 not in d
    assert 'b' not in d

    d['b'] = 2
    assert len(d) == 2
    assert list(d.keys()) == ['a', 'b']

    try:
        d['c'] = 'c'
    except TypeError:
        pass
    else:
        assert False, "TypedDict should only allow one type"


def test_typeddict_3():
    d = Wafers.TypedDict(required_type=int)
    d['a'] = 1
    assert len(d) == 1
    try:
        d['b'] = 2.0
    except TypeError:
        pass
    else:
        assert False, "TypedDict should only allow one type"


def test_typeddict_4():
    d = Wafers.TypedDict()
    d[1] = '1'
    d[2] = '2'

    assert list(d.keys()) == [1, 2]
    assert list(d.values()) == ['1', '2']
    assert list(d.items()) == [(1, '1'), (2, '2')]


def test_wafer_0():
    w = Wafers.Wafer('', 0)
    assert isinstance(w, Wafers.Wafer)
    assert w._l == ''
    assert w._w == 0

    w._l = 'A'
    assert w._l == 'A'

    w._w = 1
    assert w._w == 1

    assert w.radius > 0.
    assert w.edge_exclusion >= 0.
    assert not w.die


# Validate only one die per wafer for max rectangles with several aspect ratios
@pytest.mark.parametrize("aspect_ratio", [0.2, 0.5, 0.8, 1, 1.2, 2, 5])
def test_wafer_gen_1(aspect_ratio):
    w = Wafers.Wafer('', 0)

    # Usable radius.  *0.999 to avoid floating point errors
    r = 0.999 * (w.radius - w.edge_exclusion)

    # Rectangle dimensions
    angle = math.atan(aspect_ratio)
    width = 2 * r * math.cos(angle) / 10
    height = 2 * r * math.sin(angle) / 10

    w.generate_array_map(width, height)
    assert w.die_count == 1


# Validate only two die per wafer for max rectangles with several aspect ratios
@pytest.mark.parametrize("aspect_ratio", [0.5, 0.8, 1, 1.2, 2])
def test_wafer_gen_2(aspect_ratio):
    w = Wafers.Wafer('', 0)

    # Usable radius.  *0.999 to avoid floating point errors
    r = 0.999 * (w.radius - w.edge_exclusion)

    # Rectangle dimensions
    angle = math.atan(aspect_ratio)
    width = 2 * r * math.cos(angle) / 10
    height = 2 * r * math.sin(angle) / 10

    w.generate_array_map(width, height / 2)
    assert w.die_count == 2

    w.generate_array_map(width / 2, height)
    assert w.die_count == 2


def test_wafer_deepcopy_0():
    w1 = Wafers.Wafer('', 0)

    w1.radius = 100  # Force known radius
    w1.generate_array_map(10, 10)

    # All bad die
    for d in w1.die.values(): d.bin = 8

    die_count = w1.die_count  # Store die count

    w2 = w1.__deepcopy__()  # Copy w1 & validate data
    assert w2.die_count == die_count
    assert w2.radius == 100
    for d in w2.die.values(): assert d.bin == 8

    w1.generate_array_map(5, 5)  # Remap w1, die count changes
    w1.radius = 10

    # Die counts differ
    assert w1.die_count > die_count
    assert w2.die_count == die_count

    # Radius values differ
    assert w1.radius == 10
    assert w2.radius == 100

    # w1 all good bins, w2 all bad bins
    for d in w1.die.values(): assert d.bin == 1
    for d in w2.die.values(): assert d.bin == 8


def test_wafer_params_0():
    # Updating params with list of same length
    w = Wafers.Wafer('', 0)
    w.generate_array_map(5, 5)
    try:
        num = len(w)
    except TypeError:
        assert False, "Wafer class should implement __len__ function"
    else:
        pass

    values = np.random.uniform(size=num)

    try:
        w.set_param_vector(values)
    except:
        assert False, "Wafer class set_param_vector() broke"
    else:
        pass

    for a, b in zip(w.die_param_vector(), values):
        assert a == b, "Wafer class did not update param data correctly"

    try:
        w.set_param_vector(values[1:])
    except IndexError:
        pass
    else:
        assert False, "Wafer class set_param_vector() should reject a list of incorrect length"


def test_wafer_params_1():
    # Updating params with dict
    w = Wafers.Wafer('', 0)
    w.generate_array_map(5, 5)

    num = len(w)

    dice = copy.deepcopy(w.die)
    dice._type = np.float  # Break the TypedDict, but we will fix it...
    for key in dice.keys():
        dice[key] = np.float(np.random.uniform())

    # dice is now a TypedDict with random float values

    try:
        w.set_param_vector(dice)
    except:
        assert False, "Wafer class set_param_vector() broke"
    else:
        pass

    for a, b in zip(w.die_param_vector(), dice):
        assert a == b, "Wafer class did not update param data correctly"



