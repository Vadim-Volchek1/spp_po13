import sys
import time
import pytest
from py2 import is_palindrome, is_palindrome_alternative, get_palindrome_info

class TestIsPalindromeCore:
    """Core tests for is_palindrome function - positive and negative cases"""

    # === Positive Cases (Should return True) ===

    def test_single_digit_numbers(self):
        """Test: Single digit numbers are always palindromes"""
        for i in range(10):
            assert is_palindrome(i) is True
        assert is_palindrome(0) is True
        assert is_palindrome(5) is True
        assert is_palindrome(9) is True

    def test_two_digit_palindromes(self):
        """Test: Two-digit palindromes (11, 22, 33, etc.)"""
        palindromes = [11, 22, 33, 44, 55, 66, 77, 88, 99]
        for num in palindromes:
            assert is_palindrome(num) is True

    def test_three_digit_palindromes(self):
        """Test: Three-digit palindromes (101, 111, 121, etc.)"""
        palindromes = [101, 111, 121, 131, 202, 999]
        for num in palindromes:
            assert is_palindrome(num) is True

    def test_four_digit_palindromes(self):
        """Test: Four-digit palindromes"""
        palindromes = [1001, 1111, 1221, 2002, 9999]
        for num in palindromes:
            assert is_palindrome(num) is True

    def test_five_digit_palindromes(self):
        """Test: Five-digit palindromes"""
        palindromes = [12321, 13531, 10001, 99999]
        for num in palindromes:
            assert is_palindrome(num) is True

    def test_large_palindromes(self):
        """Test: Large palindrome numbers"""
        assert is_palindrome(123454321) is True
        assert is_palindrome(12345678900987654321) is True

    def test_palindrome_with_zeros(self):
        """Test: Palindromes containing zeros"""
        zeros_pals = [101, 1001, 10001, 1000001]
        for num in zeros_pals:
            assert is_palindrome(num) is True

    def test_zero_is_palindrome(self):
        """Test: Zero is a palindrome"""
        assert is_palindrome(0) is True

    # === Negative Cases (Should return False) ===

    def test_two_digit_non_palindromes(self):
        """Test: Two-digit non-palindromes"""
        non_pals = [10, 12, 23, 98]
        for num in non_pals:
            assert is_palindrome(num) is False

    def test_three_digit_non_palindromes(self):
        """Test: Three-digit non-palindromes"""
        non_pals = [123, 456, 789, 100, 120]
        for num in non_pals:
            assert is_palindrome(num) is False

    def test_negative_numbers(self):
        """Test: Negative numbers are not palindromes (due to minus sign)"""
        negatives = [-1, -11, -121, -12321]
        for num in negatives:
            assert is_palindrome(num) is False

    def test_numbers_ending_with_zero(self):
        """Test: Numbers ending with zero (except zero itself)"""
        ending_zero = [10, 20, 100, 1000]
        for num in ending_zero:
            assert is_palindrome(num) is False


class TestIsPalindromeBoundary:
    """Boundary and edge cases for is_palindrome function"""

    def test_minimum_integer(self):
        """Test: Minimum integer value"""
        min_int = -sys.maxsize - 1
        assert is_palindrome(min_int) is False

    def test_maximum_integer(self):
        """Test: Maximum integer value"""
        max_int = sys.maxsize
        assert is_palindrome(max_int) is False

    def test_large_numbers(self):
        """Test: Very large numbers"""
        assert is_palindrome(12345678987654321) is True
        assert is_palindrome(12345678987654320) is False

    def test_power_of_ten(self):
        """Test: Powers of ten (except 10^0 = 1)"""
        assert is_palindrome(1) is True
        for num in [10, 100, 1000, 10000]:
            assert is_palindrome(num) is False

    def test_consecutive_palindromes(self):
        """Test: Sequence of consecutive palindromes"""
        palindromes = [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            11,
            22,
            33,
            44,
            55,
            66,
            77,
            88,
            99,
            101,
        ]
        for num in palindromes:
            assert is_palindrome(num) is True

        non_palindromes = [10, 12, 20, 21, 100, 102, 110, 120]
        for num in non_palindromes:
            assert is_palindrome(num) is False

    def test_palindrome_primes(self):
        """Test: Prime palindromes"""
        prime_pals = [2, 3, 5, 7, 11, 101, 131, 151, 181, 191, 313, 353, 373, 383, 727]
        for num in prime_pals:
            assert is_palindrome(num) is True

    def test_all_same_digits(self):
        """Test: All digits the same"""
        same_digits = [111, 222, 333, 4444, 55555]
        for num in same_digits:
            assert is_palindrome(num) is True

    def test_alternating_digits(self):
        """Test: Alternating digits"""
        alternating = [1212, 123123, 121212]
        for num in alternating:
            assert is_palindrome(num) is False

    def test_32bit_boundaries(self):
        """Test: 32-bit integer boundaries"""
        assert is_palindrome(2147483647) is False
        assert is_palindrome(-2147483648) is False


class TestIsPalindromeErrors:
    """Error handling tests for is_palindrome function"""

    def test_float_input_raises_type_error(self):
        """Test: Float input raises TypeError"""
        with pytest.raises(TypeError, match="Input must be an integer"):
            is_palindrome(121.0)

    def test_string_input_raises_type_error(self):
        """Test: String input raises TypeError"""
        with pytest.raises(TypeError, match="Input must be an integer"):
            is_palindrome("121")

    def test_none_input_raises_type_error(self):
        """Test: None input raises TypeError"""
        with pytest.raises(TypeError, match="Input must be an integer"):
            is_palindrome(None)

    def test_list_input_raises_type_error(self):
        """Test: List input raises TypeError"""
        with pytest.raises(TypeError, match="Input must be an integer"):
            is_palindrome([1, 2, 1])


class TestIsPalindromeParameterized:
    """Parameterized tests for is_palindrome function"""

    @pytest.mark.parametrize(
        "number,expected",
        [
            (0, True),
            (1, True),
            (5, True),
            (9, True),
            (11, True),
            (22, True),
            (99, True),
            (10, False),
            (12, False),
            (98, False),
            (101, True),
            (111, True),
            (121, True),
            (131, True),
            (202, True),
            (999, True),
            (100, False),
            (123, False),
            (1001, True),
            (1111, True),
            (1221, True),
            (2002, True),
            (9999, True),
            (1000, False),
            (1234, False),
            (12321, True),
            (13531, True),
            (10001, True),
            (99999, True),
            (-1, False),
            (-11, False),
            (-121, False),
            (-12321, False),
            (123454321, True),
            (12345654321, True),
            (12345678987654321, True),
        ],
    )
    def test_parameterized_palindromes(self, number, expected):
        """Parameterized test for various numbers"""
        if expected:
            assert is_palindrome(number) is True
        else:
            assert is_palindrome(number) is False


class TestIsPalindromeAlternative:
    """Tests for alternative mathematical implementation"""

    def test_alternative_vs_original(self):
        """Test that alternative implementation matches original"""
        test_numbers = [0, 1, 10, 11, 121, 123, -121, 1001, 12321, 12345]
        for num in test_numbers:
            assert is_palindrome_alternative(num) == is_palindrome(num)

    def test_alternative_negative_numbers(self):
        """Test alternative with negative numbers"""
        assert is_palindrome_alternative(-121) is False
        assert is_palindrome_alternative(-11) is False

    def test_alternative_single_digit(self):
        """Test alternative with single digits"""
        for i in range(10):
            assert is_palindrome_alternative(i) is True

    def test_alternative_large_numbers(self):
        """Test alternative with large numbers"""
        assert is_palindrome_alternative(12345678987654321) is True
        assert is_palindrome_alternative(12345678987654320) is False


class TestGetPalindromeInfo:
    """Tests for palindrome information function"""

    def test_info_return_type(self):
        """Test that info returns dictionary with correct keys"""
        info = get_palindrome_info(121)
        assert isinstance(info, dict)
        expected_keys = [
            "number",
            "is_palindrome",
            "as_string",
            "reversed_string",
            "length",
            "absolute_value",
            "is_negative",
        ]
        for key in expected_keys:
            assert key in info

    def test_info_values_palindrome(self):
        """Test info values for palindrome number"""
        info = get_palindrome_info(121)
        assert info["number"] == 121
        assert info["is_palindrome"] is True
        assert info["as_string"] == "121"
        assert info["reversed_string"] == "121"
        assert info["length"] == 3
        assert info["absolute_value"] == 121
        assert info["is_negative"] is False

    def test_info_values_non_palindrome(self):
        """Test info values for non-palindrome number"""
        info = get_palindrome_info(123)
        assert info["number"] == 123
        assert info["is_palindrome"] is False
        assert info["as_string"] == "123"
        assert info["reversed_string"] == "321"
        assert info["length"] == 3
        assert info["absolute_value"] == 123
        assert info["is_negative"] is False

    def test_info_values_negative(self):
        """Test info values for negative number"""
        info = get_palindrome_info(-121)
        assert info["number"] == -121
        assert info["is_palindrome"] is False
        assert info["as_string"] == "-121"
        assert info["reversed_string"] == "121-"
        assert info["length"] == 4
        assert info["absolute_value"] == 121
        assert info["is_negative"] is True

    def test_info_zero(self):
        """Test info values for zero"""
        info = get_palindrome_info(0)
        assert info["number"] == 0
        assert info["is_palindrome"] is True
        assert info["as_string"] == "0"
        assert info["reversed_string"] == "0"
        assert info["length"] == 1
        assert info["absolute_value"] == 0
        assert info["is_negative"] is False


class TestPerformance:
    """Performance tests for palindrome checking"""

    def test_performance_large_palindrome(self):
        """Test performance with large palindrome"""
        large_pal = 12345678900987654321
        start_time = time.time()
        result = is_palindrome(large_pal)
        end_time = time.time()
        assert result is True
        assert end_time - start_time < 0.001

    def test_performance_many_numbers(self):
        """Test performance with many numbers"""
        numbers = list(range(10000))
        start_time = time.time()
        results = [is_palindrome(n) for n in numbers]
        end_time = time.time()
        assert len(results) == 10000
        assert end_time - start_time < 0.1


# === Educational Test (not counted as class method) ===


def test_educational_examples():
    """Educational test showing how palindrome checking works"""
    print("\n" + "=" * 70)
    print("Understanding Palindrome Checking")
    print("=" * 70)

    examples = [
        (121, True, "Reads same forwards and backwards"),
        (123, False, "123 forwards ≠ 321 backwards"),
        (0, True, "Single digit is always palindrome"),
        (-121, False, "Negative sign breaks palindrome property"),
        (11, True, "Two identical digits"),
        (1001, True, "Symmetric around center"),
        (10, False, "Ends with zero (except zero itself)"),
    ]

    for num, expected, reason in examples:
        result = is_palindrome(num)
        status = "✓" if result == expected else "✗"
        print(f"\n{status} is_palindrome({num}) = {result}")
        print(f"   Expected: {expected}")
        print(f"   Reason: {reason}")
        print(f"   String: '{str(num)}'")
        print(f"   Reversed: '{str(num)[::-1]}")


if __name__ == "__main__":
    test_educational_examples()

    print("\n" + "=" * 70)
    print("Running Palindrome Tests")
    print("=" * 70 + "\n")

    exit_code = pytest.main([__file__, "-v", "--tb=short", "-s"])

    print("\n" + "=" * 70)
    if exit_code == 0:
        print("✓ All tests passed successfully!")
        print("\n📊 Summary of palindrome function behavior:")
        print("   • Single digit numbers (0-9) are always palindromes")
        print("   • Negative numbers are NOT palindromes (due to minus sign)")
        print("   • Numbers ending with 0 (except 0 itself) are NOT palindromes")
        print("   • Float, string, None, list inputs raise TypeError")
        print("   • Function returns boolean True/False")
    else:
        print(f"✗ Tests failed with exit code: {exit_code}")
    print("=" * 70)

    input("\nPress Enter to exit...")
    sys.exit(exit_code)
