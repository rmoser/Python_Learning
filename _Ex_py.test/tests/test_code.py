# testing of code.py

from code import sumof

def test_sumof():
    assert sumof(0) == 0

    assert sumof(0, 1) == 1

def test_sumof2():
    assert sumof(1, 2, 3) == 6

