import pytest
from a1 import calculate_range, parse_numbers_input
from a2 import find_longest_common_prefix, parse_strings_input


class TestCalculateRange:
    def test_normal_numbers(self):
        min_val, max_val, range_val = calculate_range([1, 2, 3, 4, 5])
        assert min_val == 1
        assert max_val == 5
        assert range_val == 4

    def test_negative_numbers(self):
        min_val, max_val, range_val = calculate_range([-10, -5, 0, 5, 10])
        assert min_val == -10
        assert max_val == 10
        assert range_val == 20

    def test_single_number(self):
        min_val, max_val, range_val = calculate_range([42])
        assert min_val == 42
        assert max_val == 42
        assert range_val == 0

    def test_all_same_numbers(self):
        min_val, max_val, range_val = calculate_range([5, 5, 5, 5])
        assert min_val == 5
        assert max_val == 5
        assert range_val == 0

    def test_empty_list(self):
        with pytest.raises(ValueError, match="Последовательность пустая"):
            calculate_range([])

    def test_large_numbers(self):
        min_val, max_val, range_val = calculate_range([-1000000, 0, 1000000])
        assert min_val == -1000000
        assert max_val == 1000000
        assert range_val == 2000000


class TestParseNumbersInput:
    def test_valid_input(self):
        numbers = parse_numbers_input("1 2 3 4 5")
        assert numbers == [1, 2, 3, 4, 5]

    def test_valid_input_with_negative(self):
        numbers = parse_numbers_input("-5 0 5 10")
        assert numbers == [-5, 0, 5, 10]

    def test_empty_input(self):
        numbers = parse_numbers_input("")
        assert numbers == []

    def test_single_number(self):
        numbers = parse_numbers_input("42")
        assert numbers == [42]

    def test_invalid_input_letters(self):
        with pytest.raises(ValueError,
                           match="Последовательность некорректна - введите целые числа!"):
            parse_numbers_input("1 2 a b 5")

    def test_invalid_input_mixed(self):
        with pytest.raises(ValueError,
                           match="Последовательность некорректна - введите целые числа!"):
            parse_numbers_input("1 2 3.5 4")


class TestFindLongestCommonPrefix:
    def test_normal_strings(self):
        result = find_longest_common_prefix(["flower", "flow", "flight"])
        assert result == "fl"

    def test_no_common_prefix(self):
        result = find_longest_common_prefix(["dog", "racecar", "car"])
        assert result == ""

    def test_all_identical(self):
        result = find_longest_common_prefix(["test", "test", "test"])
        assert result == "test"

    def test_one_string(self):
        result = find_longest_common_prefix(["hello"])
        assert result == "hello"

    def test_empty_list(self):
        result = find_longest_common_prefix([])
        assert result == ""

    def test_empty_strings(self):
        result = find_longest_common_prefix(["", "", ""])
        assert result == ""

    def test_different_lengths(self):
        result = find_longest_common_prefix(["python", "py", "pytest"])
        assert result == "py"

    def test_numbers_as_strings(self):
        result = find_longest_common_prefix(["123", "12", "1234"])
        assert result == "12"

    def test_case_sensitive(self):
        result = find_longest_common_prefix(["Hello", "hello", "HELLO"])
        assert result == ""

    def test_special_characters(self):
        result = find_longest_common_prefix(["!@#", "!@#123", "!@#abc"])
        assert result == "!@#"

    def test_long_prefix(self):
        result = find_longest_common_prefix(["abcdef", "abcde", "abcd"])
        assert result == "abcd"

    def test_prefix_only_in_some(self):
        result = find_longest_common_prefix(["prefix123", "prefix456", "other"])
        assert result == ""


class TestParseStringsInput:
    def test_valid_input(self):
        strings = parse_strings_input("hello world python")
        assert strings == ["hello", "world", "python"]

    def test_empty_input(self):
        strings = parse_strings_input("")
        assert strings == []

    def test_single_string(self):
        strings = parse_strings_input("hello")
        assert strings == ["hello"]

    def test_strings_with_numbers(self):
        strings = parse_strings_input("test123 test456")
        assert strings == ["test123", "test456"]

    def test_multiple_spaces(self):
        strings = parse_strings_input("hello    world   python")
        assert strings == ["hello", "world", "python"]


class TestIntegration:
    def test_calculate_range_integration(self):
        numbers = parse_numbers_input("10 20 30 40 50")
        min_val, max_val, range_val = calculate_range(numbers)
        assert min_val == 10
        assert max_val == 50
        assert range_val == 40

    def test_find_longest_common_prefix_integration(self):
        strings = parse_strings_input("flower flow flight")
        prefix = find_longest_common_prefix(strings)
        assert prefix == "fl"

    def test_calculate_range_with_negative_integration(self):
        numbers = parse_numbers_input("-100 -50 0 50")
        min_val, max_val, range_val = calculate_range(numbers)
        assert min_val == -100
        assert max_val == 50
        assert range_val == 150

    def test_empty_input_integration(self):
        numbers = parse_numbers_input("")
        with pytest.raises(ValueError, match="Последовательность пустая"):
            calculate_range(numbers)
