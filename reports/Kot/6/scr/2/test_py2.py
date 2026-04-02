import pytest
from py2 import is_palindrome, is_palindrome_alternative, get_palindrome_info


class TestIsPalindrome:
    """
    Comprehensive test suite for is_palindrome function.
    Tests normal cases, edge cases, boundary conditions, and error handling.
    """

    # === Positive Cases (Should return True) ===

    def test_single_digit_numbers(self):
        """Test: Single digit numbers are always palindromes"""
        for i in range(10):
            assert is_palindrome(i) == True
        assert is_palindrome(0) == True
        assert is_palindrome(5) == True
        assert is_palindrome(9) == True

    def test_two_digit_palindromes(self):
        """Test: Two-digit palindromes (11, 22, 33, etc.)"""
        assert is_palindrome(11) == True
        assert is_palindrome(22) == True
        assert is_palindrome(33) == True
        assert is_palindrome(44) == True
        assert is_palindrome(55) == True
        assert is_palindrome(66) == True
        assert is_palindrome(77) == True
        assert is_palindrome(88) == True
        assert is_palindrome(99) == True

    def test_three_digit_palindromes(self):
        """Test: Three-digit palindromes (101, 111, 121, etc.)"""
        assert is_palindrome(101) == True
        assert is_palindrome(111) == True
        assert is_palindrome(121) == True
        assert is_palindrome(131) == True
        assert is_palindrome(202) == True
        assert is_palindrome(999) == True

    def test_four_digit_palindromes(self):
        """Test: Four-digit palindromes"""
        assert is_palindrome(1001) == True
        assert is_palindrome(1111) == True
        assert is_palindrome(1221) == True
        assert is_palindrome(2002) == True
        assert is_palindrome(9999) == True

    def test_five_digit_palindromes(self):
        """Test: Five-digit palindromes"""
        assert is_palindrome(12321) == True
        assert is_palindrome(13531) == True
        assert is_palindrome(10001) == True
        assert is_palindrome(99999) == True

    def test_large_palindromes(self):
        """Test: Large palindrome numbers"""
        assert is_palindrome(123454321) == True
        assert is_palindrome(12345678900987654321) == True

    def test_palindrome_with_zeros(self):
        """Test: Palindromes containing zeros"""
        assert is_palindrome(101) == True
        assert is_palindrome(1001) == True
        assert is_palindrome(10001) == True
        assert is_palindrome(1000001) == True

    def test_zero_is_palindrome(self):
        """Test: Zero is a palindrome"""
        assert is_palindrome(0) == True

    # === Negative Cases (Should return False) ===

    def test_two_digit_non_palindromes(self):
        """Test: Two-digit non-palindromes"""
        assert is_palindrome(10) == False
        assert is_palindrome(12) == False
        assert is_palindrome(23) == False
        assert is_palindrome(98) == False

    def test_three_digit_non_palindromes(self):
        """Test: Three-digit non-palindromes"""
        assert is_palindrome(123) == False
        assert is_palindrome(456) == False
        assert is_palindrome(789) == False
        assert is_palindrome(100) == False
        assert is_palindrome(120) == False

    def test_negative_numbers(self):
        """Test: Negative numbers are not palindromes (due to minus sign)"""
        assert is_palindrome(-1) == False
        assert is_palindrome(-11) == False
        assert is_palindrome(-121) == False
        assert is_palindrome(-12321) == False

    def test_numbers_ending_with_zero(self):
        """Test: Numbers ending with zero (except zero itself)"""
        assert is_palindrome(10) == False
        assert is_palindrome(20) == False
        assert is_palindrome(100) == False
        assert is_palindrome(1000) == False

    # === Edge Cases ===

    def test_minimum_integer(self):
        """Test: Minimum integer value"""
        import sys

        min_int = -sys.maxsize - 1
        assert is_palindrome(min_int) == False

    def test_maximum_integer(self):
        """Test: Maximum integer value"""
        import sys

        max_int = sys.maxsize
        assert is_palindrome(max_int) == False

    def test_large_numbers(self):
        """Test: Very large numbers"""
        large_num = 12345678987654321
        assert is_palindrome(large_num) == True

        large_non_pal = 12345678987654320
        assert is_palindrome(large_non_pal) == False

    # === Error Cases ===

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

    # === Parameterized Tests - Without Boolean Values ===

    @pytest.mark.parametrize(
        "number,expected",
        [
            # Single digit
            (0, True),
            (1, True),
            (5, True),
            (9, True),
            # Two digit
            (11, True),
            (22, True),
            (99, True),
            (10, False),
            (12, False),
            (98, False),
            # Three digit
            (101, True),
            (111, True),
            (121, True),
            (131, True),
            (202, True),
            (999, True),
            (100, False),
            (123, False),
            (456, False),
            # Four digit
            (1001, True),
            (1111, True),
            (1221, True),
            (2002, True),
            (9999, True),
            (1000, False),
            (1234, False),
            # Five digit
            (12321, True),
            (13531, True),
            (10001, True),
            (99999, True),
            (12345, False),
            # Negative numbers
            (-1, False),
            (-11, False),
            (-121, False),
            (-12321, False),
            # Large numbers
            (123454321, True),
            (12345654321, True),
            (12345678987654321, True),
        ],
    )
    def test_parameterized_palindromes(self, number, expected):
        """Parameterized test for various numbers"""
        assert is_palindrome(number) == expected

    # === Special Cases ===

    def test_palindrome_with_leading_zeros_not_applicable(self):
        """Test: Numbers don't have leading zeros in integer form"""
        assert is_palindrome(10) == False

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
            assert is_palindrome(num) == True

        non_palindromes = [10, 12, 20, 21, 100, 102, 110, 120]
        for num in non_palindromes:
            assert is_palindrome(num) == False

    def test_power_of_ten(self):
        """Test: Powers of ten (except 10^0 = 1)"""
        assert is_palindrome(1) == True
        assert is_palindrome(10) == False
        assert is_palindrome(100) == False
        assert is_palindrome(1000) == False
        assert is_palindrome(10000) == False


class TestIsPalindromeAlternative:
    """Tests for alternative mathematical implementation"""

    def test_alternative_vs_original(self):
        """Test that alternative implementation matches original"""
        test_numbers = [0, 1, 10, 11, 121, 123, -121, 1001, 12321, 12345]

        for num in test_numbers:
            assert is_palindrome_alternative(num) == is_palindrome(num)

    def test_alternative_negative_numbers(self):
        """Test alternative with negative numbers"""
        assert is_palindrome_alternative(-121) == False
        assert is_palindrome_alternative(-11) == False

    def test_alternative_single_digit(self):
        """Test alternative with single digits"""
        for i in range(10):
            assert is_palindrome_alternative(i) == True

    def test_alternative_large_numbers(self):
        """Test alternative with large numbers"""
        assert is_palindrome_alternative(12345678987654321) == True
        assert is_palindrome_alternative(12345678987654320) == False


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
        assert info["is_palindrome"] == True
        assert info["as_string"] == "121"
        assert info["reversed_string"] == "121"
        assert info["length"] == 3
        assert info["absolute_value"] == 121
        assert info["is_negative"] == False

    def test_info_values_non_palindrome(self):
        """Test info values for non-palindrome number"""
        info = get_palindrome_info(123)

        assert info["number"] == 123
        assert info["is_palindrome"] == False
        assert info["as_string"] == "123"
        assert info["reversed_string"] == "321"
        assert info["length"] == 3
        assert info["absolute_value"] == 123
        assert info["is_negative"] == False

    def test_info_values_negative(self):
        """Test info values for negative number"""
        info = get_palindrome_info(-121)

        assert info["number"] == -121
        assert info["is_palindrome"] == False
        assert info["as_string"] == "-121"
        assert info["reversed_string"] == "121-"
        assert info["length"] == 4
        assert info["absolute_value"] == 121
        assert info["is_negative"] == True

    def test_info_zero(self):
        """Test info values for zero"""
        info = get_palindrome_info(0)

        assert info["number"] == 0
        assert info["is_palindrome"] == True
        assert info["as_string"] == "0"
        assert info["reversed_string"] == "0"
        assert info["length"] == 1
        assert info["absolute_value"] == 0
        assert info["is_negative"] == False


# === Trivial and Edge Cases Focused Tests ===


class TestTrivialAndEdgeCases:
    """Special focus on trivial and edge cases"""

    def test_trivial_zero(self):
        """Trivial case: Zero"""
        assert is_palindrome(0) == True

    def test_trivial_one(self):
        """Trivial case: One"""
        assert is_palindrome(1) == True

    def test_trivial_negative_one(self):
        """Trivial case: Negative one"""
        assert is_palindrome(-1) == False

    def test_edge_two_digit_same(self):
        """Edge case: Two digits same"""
        assert is_palindrome(11) == True

    def test_edge_two_digit_different(self):
        """Edge case: Two digits different"""
        assert is_palindrome(12) == False

    def test_edge_power_of_two(self):
        """Edge case: Powers of two"""
        assert is_palindrome(2) == True
        assert is_palindrome(4) == True
        assert is_palindrome(8) == True
        assert is_palindrome(16) == False
        assert is_palindrome(32) == False
        assert is_palindrome(64) == False
        assert is_palindrome(128) == False
        assert is_palindrome(256) == False
        assert is_palindrome(512) == False

    def test_edge_palindrome_primes(self):
        """Edge case: Prime palindromes"""
        prime_palindromes = [
            2,
            3,
            5,
            7,
            11,
            101,
            131,
            151,
            181,
            191,
            313,
            353,
            373,
            383,
            727,
        ]
        for num in prime_palindromes:
            assert is_palindrome(num) == True

    def test_edge_all_same_digits(self):
        """Edge case: All digits the same"""
        assert is_palindrome(111) == True
        assert is_palindrome(222) == True
        assert is_palindrome(333) == True
        assert is_palindrome(4444) == True
        assert is_palindrome(55555) == True

    def test_edge_alternating_digits(self):
        """Edge case: Alternating digits"""
        assert is_palindrome(1212) == False
        assert is_palindrome(123123) == False
        assert is_palindrome(121212) == False

    def test_edge_very_large_palindrome(self):
        """Edge case: Very large palindrome"""
        real_large_pal = 12345678900987654321
        assert is_palindrome(real_large_pal) == True

    def test_edge_max_32bit_int(self):
        """Edge case: Maximum 32-bit integer (2,147,483,647)"""
        max_32bit = 2147483647
        assert is_palindrome(max_32bit) == False

    def test_edge_min_32bit_int(self):
        """Edge case: Minimum 32-bit integer (-2,147,483,648)"""
        min_32bit = -2147483648
        assert is_palindrome(min_32bit) == False


# === Performance Tests ===


class TestPerformance:
    """Performance tests for palindrome checking"""

    def test_performance_large_palindrome(self):
        """Test performance with large palindrome"""
        import time

        large_pal = 12345678900987654321

        start_time = time.time()
        result = is_palindrome(large_pal)
        end_time = time.time()

        assert result == True
        assert end_time - start_time < 0.001

    def test_performance_many_numbers(self):
        """Test performance with many numbers"""
        import time

        numbers = list(range(10000))

        start_time = time.time()
        results = [is_palindrome(n) for n in numbers]
        end_time = time.time()

        assert len(results) == 10000
        assert end_time - start_time < 0.1


# === Educational Test ===


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
        print(f"   Reversed: '{str(num)[::-1]}'")


if __name__ == "__main__":
    import sys

    # Run educational test first
    test_educational_examples()

    print("\n" + "=" * 70)
    print("Running Palindrome Tests")
    print("=" * 70 + "\n")

    # Run all tests
    exit_code = pytest.main([__file__, "-v", "--tb=short", "-s"])

    print("\n" + "=" * 70)
    if exit_code == 0:
        print("✓ All tests passed successfully!")
        print("\n📊 Summary of palindrome function behavior:")
        print("   • Single digit numbers (0-9) are always palindromes")
        print("   • Negative numbers are NOT palindromes (due to minus sign)")
        print("   • Numbers ending with 0 (except 0 itself) are NOT palindromes")
        print(
            "   • Boolean values (True/False) raise TypeError (not accepted as integers)"
        )
        print("   • Float, string, None, list inputs raise TypeError")
        print("   • Function returns boolean True/False")
    else:
        print(f"✗ Tests failed with exit code: {exit_code}")
    print("=" * 70)

    input("\nPress Enter to exit...")
    sys.exit(exit_code)
