import ps5
import string


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


def test_pm0():
    m = ps5.PlaintextMessage(string.ascii_letters, 0)

    assert m.get_message_text() == string.ascii_letters
    assert m.get_message_text_encrypted() == string.ascii_letters

    m.change_shift(1)
    assert m.get_message_text() == string.ascii_letters
    assert m.get_message_text_encrypted() == string.ascii_lowercase[1:] + 'a' + string.ascii_uppercase[1:] + 'A'

    m.change_shift(3)
    assert m.get_message_text() == string.ascii_letters
    assert m.get_message_text_encrypted() == string.ascii_lowercase[3:] + 'abc' + string.ascii_uppercase[3:] + 'ABC'

    m.change_shift(0)
    assert m.get_message_text() == string.ascii_letters
    assert m.get_message_text_encrypted() == string.ascii_letters


def test_CiphertextMessage():
    assert ps5.CiphertextMessage('jgnnq').decrypt_message() == (24, 'hello')
    assert ps5.CiphertextMessage('JGNNQ').decrypt_message() == (24, 'HELLO')
    assert ps5.CiphertextMessage('zdqghuoxvw').decrypt_message() == (23, 'wanderlust')
    assert ps5.CiphertextMessage('JGNNQ 55').decrypt_message() == (24, 'HELLO 55')

