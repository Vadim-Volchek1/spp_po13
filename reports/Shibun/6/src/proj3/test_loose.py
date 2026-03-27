import pytest # type: ignore
from loose import loose


#  ТЕСТЫ ПО СПЕЦИФИКАЦИИ
def test_loose_none_none():
    with pytest.raises(TypeError):
        loose(None, None)


def test_loose_none_any():
    assert loose(None, "abc") is None


def test_loose_empty_any():
    assert loose("", "abc") == ""


def test_loose_any_none():
    assert loose("hello", None) == "hello"


def test_loose_any_empty():
    assert loose("hello", "") == "hello"


def test_loose_example_1():
    assert loose(" hello ", "hl") == "eo"


def test_loose_example_2():
    assert loose(" hello ", "le") == "ho"


#  ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ
def test_loose_no_common_chars():
    assert loose("abc", "xyz") == "abc"


def test_loose_remove_all():
    assert loose("aaa", "a") == ""


def test_loose_case_sensitive():
    assert loose("AaA", "a") == "AA"   # 'a' != 'A'


def test_loose_non_string_first():
    with pytest.raises(TypeError):
        loose(123, "abc")


def test_loose_non_string_second():
    with pytest.raises(TypeError):
        loose("abc", 123)
