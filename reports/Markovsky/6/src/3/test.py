# pylint: disable=too-many-public-methods
import pytest
from string_diff import index_of_difference


class TestIndexOfDifference:
    def test_both_none(self):
        with pytest.raises(TypeError, match="Arguments cannot be None"):
            index_of_difference(None, None)

    def test_first_none(self):
        with pytest.raises(TypeError, match="Arguments cannot be None"):
            index_of_difference(None, "abc")

    def test_second_none(self):
        with pytest.raises(TypeError, match="Arguments cannot be None"):
            index_of_difference("abc", None)

    def test_both_empty(self):
        result = index_of_difference("", "")
        assert result == -1

    def test_first_empty_second_not_empty(self):
        result = index_of_difference("", "abc")
        assert result == 0

    def test_second_empty_first_not_empty(self):
        result = index_of_difference("abc", "")
        assert result == 0

    def test_identical_strings(self):
        result = index_of_difference("abc", "abc")
        assert result == -1

    def test_identical_with_spaces(self):
        result = index_of_difference("abc ", " abc")
        assert result == -1

    def test_different_at_beginning(self):
        result = index_of_difference("abc", "xyz")
        assert result == 0

    def test_different_in_middle(self):
        result = index_of_difference("i am a machine", "i am a robot")
        assert result == 7

    def test_different_at_end(self):
        result = index_of_difference("abcde", "abcdf")
        assert result == 4

    def test_different_lengths_short_first(self):
        result = index_of_difference("ab", "abxyz")
        assert result == 2

    def test_different_lengths_short_second(self):
        result = index_of_difference("abcde", "abc")
        assert result == 3

    def test_different_lengths_with_diff_before_end(self):
        result = index_of_difference("abcd", "abxy")
        assert result == 2

    def test_specification_example_1(self):
        result = index_of_difference("abc ", " abc")
        assert result == -1

    def test_specification_example_2(self):
        result = index_of_difference("ab", " abxyz")
        assert result == 2

    def test_specification_example_3(self):
        result = index_of_difference(" abcde ", " abxyz ")
        assert result == 2

    def test_specification_example_4(self):
        result = index_of_difference(" abcde ", "xyz")
        assert result == 0

    def test_unicode_strings(self):
        result = index_of_difference("привет", "привет")
        assert result == -1

        result = index_of_difference("привет мир", "привет мир!")
        assert result == 10

    def test_numeric_strings(self):
        result = index_of_difference("12345", "12345")
        assert result == -1

        result = index_of_difference("12345", "12346")
        assert result == 4

    def test_case_sensitive(self):
        result = index_of_difference("Hello", "hello")
        assert result == 0

    def test_special_characters(self):
        result = index_of_difference("!@#$%", "!@#$%")
        assert result == -1

        result = index_of_difference("!@#$%", "!@#^%")
        assert result == 3

    def test_very_long_strings(self):
        long_str1 = "a" * 10000
        long_str2 = "a" * 9999 + "b"
        result = index_of_difference(long_str1, long_str2)
        assert result == 9999
