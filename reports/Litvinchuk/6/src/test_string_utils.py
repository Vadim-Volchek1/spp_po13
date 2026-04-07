import pytest
from string_utils import keep


def test_keep_none_none():
    with pytest.raises(TypeError):
        keep(None, None)


def test_keep_none_pattern():
    assert keep(None, "abc") is None


def test_keep_empty_string():
    assert keep("", "abc") == ""


def test_keep_pattern_none():
    assert keep("hello", None) == ""


def test_keep_pattern_empty():
    assert keep("hello", "") == ""


def test_keep_hl():
    assert keep(" hello ", "hl") == " hll "


def test_keep_le():
    assert keep(" hello ", "le") == " ell "


def test_keep_no_matches():
    assert keep("abc", "xyz") == ""


def test_keep_all_matches():
    assert keep("abc", "abc") == "abc"


def test_keep_repeated_chars():
    assert keep("hello world", "lo") == "llo ol"