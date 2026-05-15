import pytest
from string_utils import repeat


class TestRepeat:
    # Вариант 1 тесты для метода repeat(pattern, repeat)

    def test_repeat_zero_times_returns_empty_string(self):
        # repeat("e", 0) = ""
        assert repeat("e", 0) == ""

    def test_repeat_three_times(self):
        # repeat("e", 3) = "eee"
        assert repeat("e", 3) == "eee"

    def test_repeat_abc_two_times(self):
        # repeat("ABC", 2) = "ABCABC"
        assert repeat("ABC", 2) == "ABCABC"

    def test_repeat_negative_raises_valueerror(self):
        # repeat("e", -2) = ValueError
        with pytest.raises(ValueError):
            repeat("e", -2)

    def test_repeat_none_pattern_raises_typeerror(self):
        # repeat(None, 1) = TypeError
        with pytest.raises(TypeError):
            repeat(None, 1)

# Граничные случаи

    def test_repeat_empty_string(self):
        # Повторение пустой строки"""
        assert repeat("", 0) == ""
        assert repeat("", 5) == ""

    def test_repeat_one_time_returns_original(self):
        # Повторение 1 раз возвращает исходный паттерн
        assert repeat("hello", 1) == "hello"

    def test_repeat_non_int_raises_typeerror(self):
        # Нецелочисленный repeat вызывает TypeError
        with pytest.raises(TypeError):
            repeat("a", 3.5)
