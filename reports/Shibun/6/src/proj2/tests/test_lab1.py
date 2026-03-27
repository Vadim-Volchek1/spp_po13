import pytest # type: ignore
from lab1.uniq_numbers import uniq_numbers
from lab1.add_binary import addBinary


#  ТЕСТЫ uniq_numbers
def test_uniq_numbers_basic():
    assert uniq_numbers([1, 2, 3]) == {1, 2, 3}


def test_uniq_numbers_with_duplicates():
    assert uniq_numbers([1, 1, 2, 2, 3]) == {1, 2, 3}


def test_uniq_numbers_empty():
    assert uniq_numbers([]) == set()


def test_uniq_numbers_negative_values():
    assert uniq_numbers([-1, -1, -2]) == {-1, -2}


def test_uniq_numbers_mixed_types():
    assert uniq_numbers([1, "1", 1]) == {1, "1"}


#  ТЕСТЫ addBinary
def test_add_binary_basic():
    assert addBinary("11", "1") == "100"


def test_add_binary_zero():
    assert addBinary("0", "0") == "0"


def test_add_binary_large():
    assert addBinary("101010", "111") == bin(int("101010", 2) + int("111", 2))[2:]


def test_add_binary_leading_zeros():
    assert addBinary("0011", "0001") == "100"


def test_add_binary_invalid_characters():
    with pytest.raises(ValueError):
        addBinary("12", "1")   # 2 — не бинарный символ


def test_add_binary_empty_string():
    with pytest.raises(ValueError):
        addBinary("", "1")


def test_add_binary_non_string():
    with pytest.raises(TypeError):
        addBinary(11, 1) # type: ignore
