import ps5
import string

# Override file location
ps5.WORDLIST_FILENAME = r"F:\Users\Bob\Documents\Git\Python_Learning\6001x\ps5\words.txt"

def test_PlaintextMessage():
    assert ps5.PlaintextMessage('hello', 2).get_message_text_encrypted() == 'jgnnq'

def text_CiphertextMessage():
    assert ps5.CiphertextMessage('jgnnq').decrypt_message() == (24, 'hello')

def test_build_shift_dict():
    m = ps5.Message("")
    d = m.build_shift_dict(0)
    for c in string.ascii_letters:
        assert d[c] == c

    d = m.build_shift_dict(5)
    assert d['a'] == 'f'
    assert d['u'] == 'z'
    assert d['v'] == 'a'
    assert d['A'] == 'F'
    assert d['U'] == 'Z'
    assert d['V'] == 'A'

def test_apply_shift():
    m = ps5.Message("hello")

    assert m.apply_shift(0) == 'hello'
    assert m.apply_shift(1) == 'ifmmp'
    assert m.apply_shift(2) == 'jgnnq'
    assert m.apply_shift(3) == 'khoor'

    m = ps5.Message("Hawaii 5-0")
    assert m.apply_shift(0) == 'Hawaii 5-0'
    assert m.apply_shift(1) == 'Ibxbjj 5-0'
    assert m.apply_shift(2) == 'Jcyckk 5-0'
