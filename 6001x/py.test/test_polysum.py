from polysum import polysum

def test_polysum_0():
    assert polysum(0, 0) == 0
    assert polysum(1, 0) == 0
    assert polysum(0, 1) == 0
    assert polysum(21, 100) == 4758314.7412
    assert polysum(42, 68) == 8804617.4148
    assert polysum("A", 1) == 0
    assert polysum(1, "A") == 0
