# test_string_repeat.py
import pytest
from string_repeat import repeat


class TestStringRepeat:
    """
    Test class for repeat function
    Tests the specification:
    - repeat("e", 0) = ""
    - repeat("e", 3) = "eee"
    - repeat(" ABC ", 2) = " ABC  ABC "  # Fixed: two spaces between (logical concatenation)
    - repeat("e", -2) = ValueError
    - repeat(None, 1) = TypeError
    """

    # === Tests for normal cases ===

    def test_repeat_with_zero_repetitions(self):
        """Test: repeat(pattern, 0) should return empty string"""
        assert repeat("e", 0) == ""
        assert repeat("abc", 0) == ""
        assert repeat("123", 0) == ""

    def test_repeat_with_positive_repetitions(self):
        """Test: repeat(pattern, positive number) should return repeated pattern"""
        assert repeat("e", 3) == "eee"
        assert repeat("ab", 2) == "abab"
        assert repeat("123", 1) == "123"
        assert repeat(" ", 3) == "   "
        assert repeat("!@#", 2) == "!@#!@#"

    def test_repeat_with_multiple_characters(self):
        """Test: repeat with patterns containing multiple characters"""
        # Fixed: Simple concatenation of " ABC " twice gives " ABC  ABC "
        assert repeat(" ABC ", 2) == " ABC  ABC "
        assert repeat("Hello", 3) == "HelloHelloHello"
        assert repeat("Test ", 2) == "Test Test "
        assert repeat("--->", 4) == "--->--->--->--->"

    def test_repeat_with_single_character(self):
        """Test: repeat with single character patterns"""
        assert repeat("a", 5) == "aaaaa"
        assert repeat("x", 10) == "xxxxxxxxxx"
        assert repeat("1", 3) == "111"

    def test_repeat_with_whitespace(self):
        """Test: repeat with whitespace patterns"""
        assert repeat(" ", 5) == "     "
        assert repeat("\t", 2) == "\t\t"
        assert repeat("\n", 3) == "\n\n\n"
        assert repeat(" \t ", 2) == " \t  \t "

    def test_repeat_with_special_characters(self):
        """Test: repeat with special characters"""
        assert repeat("!@#$%", 2) == "!@#$%!@#$%"
        assert repeat("\\n", 3) == "\\n\\n\\n"
        assert repeat("'\"", 2) == "'\"'\""

    def test_repeat_with_unicode(self):
        """Test: repeat with unicode characters"""
        assert repeat("Привет", 2) == "ПриветПривет"
        assert repeat("😊", 3) == "😊😊😊"
        assert repeat("★", 4) == "★★★★"
        assert repeat("ño", 2) == "ñoño"

    # === Tests for error cases ===

    def test_repeat_with_negative_repetitions_raises_value_error(self):
        """Test: repeat(pattern, negative) should raise ValueError"""
        with pytest.raises(ValueError, match="repeat count must be non-negative"):
            repeat("e", -1)

        with pytest.raises(ValueError, match="repeat count must be non-negative"):
            repeat("abc", -5)

        with pytest.raises(ValueError):
            repeat("test", -2)

    def test_repeat_with_none_pattern_raises_type_error(self):
        """Test: repeat(None, n) should raise TypeError"""
        with pytest.raises(TypeError, match="pattern must be a string"):
            repeat(None, 1)

        with pytest.raises(TypeError):
            repeat(None, 5)

    def test_repeat_with_non_string_pattern_raises_type_error(self):
        """Test: repeat(non-string, n) should raise TypeError"""
        with pytest.raises(TypeError, match="pattern must be a string"):
            repeat(123, 3)

        with pytest.raises(TypeError, match="pattern must be a string"):
            repeat(3.14, 2)

        with pytest.raises(TypeError):
            repeat([1, 2, 3], 2)

        with pytest.raises(TypeError):
            repeat({"key": "value"}, 1)

    def test_repeat_with_non_integer_repetitions_raises_type_error(self):
        """Test: repeat(pattern, non-integer) should raise TypeError"""
        with pytest.raises(TypeError, match="repeat count must be an integer"):
            repeat("abc", "2")

        with pytest.raises(TypeError, match="repeat count must be an integer"):
            repeat("abc", 3.5)

        with pytest.raises(TypeError):
            repeat("abc", [1])

    # === Parameterized tests ===

    @pytest.mark.parametrize(
        "pattern,repetitions,expected",
        [
            ("e", 0, ""),
            ("e", 1, "e"),
            ("e", 3, "eee"),
            ("abc", 2, "abcabc"),
            (" ABC ", 2, " ABC  ABC "),  # Fixed: correct concatenation result
            ("", 5, ""),
            ("a", 1, "a"),
            ("ab", 3, "ababab"),
            ("123", 0, ""),
            ("!@#", 2, "!@#!@#"),
            ("\n", 2, "\n\n"),
            ("😊", 3, "😊😊😊"),
            ("Привет", 1, "Привет"),
            (" ", 3, "   "),
            (" x ", 2, " x  x "),  # This shows two spaces between " x" and "x "
        ],
    )
    def test_repeat_parameterized(self, pattern, repetitions, expected):
        """Parameterized test for various valid inputs"""
        result = repeat(pattern, repetitions)
        assert result == expected, f"Expected '{expected}', got '{result}'"

    @pytest.mark.parametrize(
        "pattern,repetitions,expected_exception,expected_message",
        [
            ("e", -1, ValueError, "repeat count must be non-negative"),
            ("abc", -5, ValueError, "repeat count must be non-negative"),
            (None, 1, TypeError, "pattern must be a string"),
            (123, 3, TypeError, "pattern must be a string"),
            (3.14, 2, TypeError, "pattern must be a string"),
            ("abc", "2", TypeError, "repeat count must be an integer"),
            ("abc", 3.5, TypeError, "repeat count must be an integer"),
        ],
    )
    def test_repeat_error_cases_parameterized(
        self, pattern, repetitions, expected_exception, expected_message
    ):
        """Parameterized test for various error cases"""
        with pytest.raises(expected_exception, match=expected_message):
            repeat(pattern, repetitions)

    # === Edge cases ===

    def test_repeat_with_empty_string_pattern(self):
        """Test: repeat("", n) should return empty string for any n >= 0"""
        assert repeat("", 0) == ""
        assert repeat("", 5) == ""
        assert repeat("", 100) == ""

    def test_repeat_with_large_repetitions(self):
        """Test: repeat with large number of repetitions"""
        pattern = "a"
        repetitions = 10000
        result = repeat(pattern, repetitions)
        assert len(result) == repetitions
        assert result == "a" * repetitions

    def test_repeat_with_complex_pattern(self):
        """Test: repeat with complex pattern"""
        pattern = "A B C"
        assert repeat(pattern, 3) == "A B CA B CA B C"
        assert repeat(pattern, 1) == "A B C"

    def test_repeat_with_pattern_containing_newlines(self):
        """Test: repeat with pattern containing newlines"""
        pattern = "Line1\n"
        assert repeat(pattern, 3) == "Line1\nLine1\nLine1\n"

    # === Tests for exact specification ===

    def test_specification_example_1(self):
        """Test specification example: repeat("e", 0) = "" """
        assert repeat("e", 0) == ""

    def test_specification_example_2(self):
        """Test specification example: repeat("e", 3) = "eee" """
        assert repeat("e", 3) == "eee"

    def test_specification_example_3(self):
        """Test specification example: repeat(" ABC ", 2) = " ABC  ABC " """
        # Fixed: The correct concatenation gives two spaces
        assert repeat(" ABC ", 2) == " ABC  ABC "

    def test_specification_example_4(self):
        """Test specification example: repeat("e", -2) = ValueError"""
        with pytest.raises(ValueError):
            repeat("e", -2)

    def test_specification_example_5(self):
        """Test specification example: repeat(None, 1) = TypeError"""
        with pytest.raises(TypeError):
            repeat(None, 1)

    # === Additional test to demonstrate the behavior ===

    def test_concatenation_behavior(self):
        """Demonstrate string concatenation behavior"""
        # Show how string multiplication works
        pattern = " ABC "
        assert pattern * 2 == " ABC  ABC "

        # Show individual characters
        assert list(pattern) == [" ", "A", "B", "C", " "]

        # First repetition: " ABC "
        # Second repetition: " ABC "
        # Result: " ABC " + " ABC " = " ABC  ABC "


# === Performance tests ===


class TestStringRepeatPerformance:
    """Performance tests for repeat function"""

    def test_repeat_performance_with_large_repetitions(self):
        """Test performance with large repetitions"""
        import time

        pattern = "test"
        repetitions = 100000

        start_time = time.time()
        result = repeat(pattern, repetitions)
        end_time = time.time()

        assert len(result) == len(pattern) * repetitions
        # Should complete in reasonable time (less than 1 second for 100k reps)
        assert end_time - start_time < 1.0

    def test_memory_efficiency(self):
        """Test that function doesn't use excessive memory"""
        import sys

        pattern = "x"
        repetitions = 1000000
        result = repeat(pattern, repetitions)

        # Memory usage should be proportional to result size
        expected_size = repetitions  # 1 byte per character (for ASCII)
        actual_size = sys.getsizeof(result)

        # Allow some overhead, but shouldn't be dramatically larger
        assert actual_size < expected_size * 1.5


# === Simple test to verify all specification requirements ===


def test_all_specification_requirements():
    """Test all requirements from the specification with corrected expectations"""

    # Requirement 1: repeat("e", 0) = ""
    assert repeat("e", 0) == ""

    # Requirement 2: repeat("e", 3) = "eee"
    assert repeat("e", 3) == "eee"

    # Requirement 3: repeat(" ABC ", 2) = " ABC  ABC " (logical concatenation)
    assert repeat(" ABC ", 2) == " ABC  ABC "

    # Requirement 4: repeat("e", -2) = ValueError
    try:
        repeat("e", -2)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Requirement 5: repeat(None, 1) = TypeError
    try:
        repeat(None, 1)
        assert False, "Should have raised TypeError"
    except TypeError:
        pass


# === Educational test to understand string multiplication ===


def test_understanding_string_multiplication():
    """Educational test to understand how string multiplication works"""

    # String multiplication simply concatenates the string with itself
    assert "ABC" * 3 == "ABCABCABC"

    # Spaces are preserved exactly as they appear
    assert " A " * 2 == " A  A "

    # Leading and trailing spaces are preserved
    pattern = "  Hello  "
    assert pattern * 2 == "  Hello    Hello  "

    # Empty string multiplication
    assert "" * 100 == ""

    # Single character
    assert "x" * 5 == "xxxxx"


if __name__ == "__main__":
    import sys

    print("\n" + "=" * 60)
    print("Running String Repeat Tests")
    print("=" * 60 + "\n")

    # Run pytest with current file
    exit_code = pytest.main([__file__, "-v", "-s", "--tb=short"])

    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✓ All tests passed successfully!")
    else:
        print(f"✗ Tests failed with exit code: {exit_code}")
    print("=" * 60)

    # Pause to view results
    input("\nPress Enter to exit...")

    sys.exit(exit_code)
