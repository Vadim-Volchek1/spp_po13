
import pytest
from lab1 import parse_int_list, digit_distribution, hamming_weight



# ТЕСТЫ ДЛЯ parse_int_list
def test_parse_int_list_valid():
    """
    Проверяем корректный случай:
    строка содержит только целые числа.
    """
    assert parse_int_list("1 2 3") == [1, 2, 3]


def test_parse_int_list_negative():
    """
    Проверяем, что отрицательные числа тоже корректно парсятся.
    """
    assert parse_int_list("-1 -2 -3") == [-1, -2, -3]


def test_parse_int_list_invalid():
    """
    Проверяем, что при наличии нечислового элемента выбрасывается ValueError.
    """
    with pytest.raises(ValueError):
        parse_int_list("10 abc 20")


def test_parse_int_list_empty_string():
    """
    Граничный случай: пустая строка → пустой список.
    """
    assert parse_int_list("") == []

# ТЕСТЫ ДЛЯ digit_distribution
def test_digit_distribution_simple():
    """
    Проверяем базовый случай:
    числа разной длины → корректное распределение.
    """
    nums = [1, 22, 333]
    assert digit_distribution(nums) == {1: 1, 2: 1, 3: 1}


def test_digit_distribution_zero():
    """
    Число 0 имеет одну цифру.
    """
    assert digit_distribution([0]) == {1: 1}


def test_digit_distribution_repeated():
    """
    Несколько чисел одинаковой длины.
    """
    nums = [5, 7, 12, 99]
    assert digit_distribution(nums) == {1: 2, 2: 2}


def test_digit_distribution_negative_numbers():
    """
    Отрицательные числа должны учитываться по количеству цифр без знака.
    """
    nums = [-1, -22, 333]
    assert digit_distribution(nums) == {1: 1, 2: 1, 3: 1}


def test_digit_distribution_empty():
    """
    Граничный случай: пустой список → пустой словарь.
    """
    assert digit_distribution([]) == {}


# ТЕСТЫ ДЛЯ hamming_weight
def test_hamming_weight_zero():
    """
    0 в двоичном виде — 0, установленных битов нет.
    """
    assert hamming_weight(0) == 0


def test_hamming_weight_normal():
    """
    Проверяем обычный случай:
    5 = 0b101 → два установленных бита.
    """
    assert hamming_weight(5) == 2


def test_hamming_weight_large():
    """
    Граничный случай: число вида 2^n - 1,
    у которого все n младших битов равны 1.
    """
    assert hamming_weight(2**10 - 1) == 10


def test_hamming_weight_negative():
    """
    Функция должна выбрасывать ValueError для отрицательных чисел.
    """
    with pytest.raises(ValueError):
        hamming_weight(-1)


def test_hamming_weight_not_int():
    """
    Функция должна выбрасывать TypeError, если аргумент не int.
    """
    with pytest.raises(TypeError):
        hamming_weight(3.14)
