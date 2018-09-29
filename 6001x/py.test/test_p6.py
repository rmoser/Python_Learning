import p6

def test_flatten_0():
    assert p6.flatten([]) == []
    assert p6.flatten([0]) == [0]
    assert p6.flatten([1]) == [1]
    assert p6.flatten([0, 1]) == [0, 1]
    assert p6.flatten([0, 2, 1]) == [0, 2, 1]
    assert p6.flatten([1, 'a', 'b,c']) == [1, 'a', 'b,c']

def test_flatten_1():
    assert p6.flatten([1, ['a', 'b,c']]) == [1, 'a', 'b,c']
    assert p6.flatten([0, [0, [0, [0, 0, 0]]]]) == [0] * 6
    assert p6.flatten([1, [0, [0, [0, 0, 0]]]]) == [1] + [0] * 5

def test_flatten_2():
    assert p6.flatten([[1,'a',['cat'],2],[[[3]],'dog'],4,5]) == [1,'a','cat',2,3,'dog',4,5]
