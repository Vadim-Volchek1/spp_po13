import pytest
from task3 import indexOfDifference


def test_both_none():
    """indexOfDifference(None, None) = TypeError"""
    with pytest.raises(TypeError):
        indexOfDifference(None, None)


def test_both_empty():
    """indexOfDifference("", "") = -1"""
    assert indexOfDifference("", "") == -1


def test_empty_and_nonempty():
    """indexOfDifference("", "abc") = 0"""
    assert indexOfDifference("", "abc") == 0


def test_nonempty_and_empty():
    """indexOfDifference("abc", "") = 0"""
    assert indexOfDifference("abc", "") == 0


def test_equal_strings():
    """indexOfDifference("abc", "abc") = -1"""
    assert indexOfDifference("abc", "abc") == -1


def test_difference_in_middle():
    """indexOfDifference("i am a machine", "i am a robot") = 7"""
    assert indexOfDifference("i am a machine", "i am a robot") == 7


def test_difference_after_prefix():
    """indexOfDifference("ab", "abxyz") = 2"""
    assert indexOfDifference("ab", "abxyz") == 2


def test_difference_after_prefix2():
    """indexOfDifference("abcde", "abxyz") = 2"""
    assert indexOfDifference("abcde", "abxyz") == 2


def test_difference_at_start():
    """indexOfDifference("abcde", "xyz") = 0"""
    assert indexOfDifference("abcde", "xyz") == 0


def test_one_char_diff():
    assert indexOfDifference("a", "b") == 0


def test_prefix_same_length():
    assert indexOfDifference("abcd", "abce") == 3


def test_longer_second():
    assert indexOfDifference("abc", "abcd") == 3


def test_longer_first():
    assert indexOfDifference("abcd", "abc") == 3
