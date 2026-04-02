import time
import sys
import pytest
from py1 import find_outlier_median, find_outlier_median_enhanced, get_statistics


class TestFindOutlierMedianCore:
    """Core tests for find_outlier_median function - normal cases."""

    # === Normal Cases ===

    def test_basic_outlier_at_end(self):
        """Test: Outlier is the largest number"""
        assert find_outlier_median([1, 2, 3, 4, 100]) == 100

    def test_basic_outlier_at_beginning(self):
        """Test: Outlier is the smallest number"""
        assert find_outlier_median([-100, 1, 2, 3, 4]) == -100

    def test_multiple_same_values(self):
        """Test: Many identical values with one outlier"""
        assert find_outlier_median([1, 1, 1, 1, 100]) == 100

    def test_negative_numbers(self):
        """Test: Sequence with negative numbers"""
        assert find_outlier_median([-10, -5, -3, -2, -1]) == -10
        assert find_outlier_median([-100, -1, -1, -1, -1]) == -100

    def test_mixed_positive_negative(self):
        """Test: Mixed positive and negative numbers"""
        assert find_outlier_median([-10, -5, 0, 5, 100]) == 100
        assert find_outlier_median([-100, 0, 0, 0, 10]) == -100

    def test_floating_point_numbers(self):
        """Test: Floating point numbers"""
        result = find_outlier_median([1.5, 2.5, 3.5, 4.5, 100.5])
        assert result == 100.5

        result2 = find_outlier_median([0.1, 0.2, 0.3, 0.4, 10.0])
        assert result2 == 10.0

    def test_all_identical_values(self):
        """Test: All values identical"""
        result = find_outlier_median([5, 5, 5, 5, 5])
        assert result == 5

    def test_two_distinct_values(self):
        """Test: Only two distinct values"""
        result = find_outlier_median([1, 1, 1, 2, 2])
        assert result == 2


class TestFindOutlierMedianEdge:
    """Edge cases for find_outlier_median function."""

    def test_single_element(self):
        """Test: Sequence with one element"""
        assert find_outlier_median([42]) == 42
        assert find_outlier_median([-5]) == -5
        assert find_outlier_median([0]) == 0

    def test_two_elements(self):
        """Test: Sequence with two elements"""
        assert find_outlier_median([1, 100]) == 1
        assert find_outlier_median([-50, 50]) == -50

    def test_three_elements(self):
        """Test: Sequence with three elements"""
        assert find_outlier_median([1, 2, 100]) == 100
        assert find_outlier_median([-100, 0, 1]) == -100
        assert find_outlier_median([10, 20, 30]) == 10

    def test_even_length_sequence(self):
        """Test: Even length sequences"""
        assert find_outlier_median([1, 2, 3, 100]) == 100
        assert find_outlier_median([1, 1, 100, 100]) == 1

    def test_large_numbers(self):
        """Test: Very large numbers"""
        assert (
            find_outlier_median([10**9, 10**9 + 1, 10**9 + 2, 10**9 + 3, 10**18])
            == 10**18
        )

    def test_small_numbers(self):
        """Test: Very small numbers"""
        assert find_outlier_median(
            [-(10**9), -(10**9) + 1, -(10**9) + 2, -(10**9) + 3, -(10**18)]
        ) == -(10**18)

    def test_unsorted_input(self):
        """Test: Unsorted input sequence"""
        assert find_outlier_median([100, 1, 3, 2, 4]) == 100
        assert find_outlier_median([50, -100, 0, 20, 30]) == -100


class TestFindOutlierMedianBoundary:
    """Boundary cases for find_outlier_median function."""

    def test_median_at_beginning(self):
        """Test: Median is the smallest value"""
        assert find_outlier_median([1, 2, 3, 4, 5]) == 1

    def test_median_at_end(self):
        """Test: Median is the largest value"""
        assert find_outlier_median([1, 1, 1, 2, 100]) == 100

    def test_two_possible_outliers_equal_distance(self):
        """Test: Two elements equally distant from median"""
        result = find_outlier_median([1, 2, 3, 4, 5])
        assert result == 1

        result = find_outlier_median([0, 0, 5, 10, 10])
        assert result == 0


class TestFindOutlierMedianErrors:
    """Error cases for find_outlier_median function."""

    def test_empty_sequence_raises_value_error(self):
        """Test: Empty sequence raises ValueError"""
        with pytest.raises(ValueError, match="Sequence cannot be empty"):
            find_outlier_median([])

    def test_none_input_raises_type_error(self):
        """Test: None input raises TypeError"""
        with pytest.raises(TypeError, match="Input must be a list or tuple"):
            find_outlier_median(None)

    def test_string_input_raises_type_error(self):
        """Test: String input raises TypeError"""
        with pytest.raises(TypeError, match="Input must be a list or tuple"):
            find_outlier_median("not a list")

    def test_list_with_strings_raises_type_error(self):
        """Test: List containing non-numeric values"""
        with pytest.raises(TypeError, match="All elements must be numbers"):
            find_outlier_median([1, 2, "three", 4])

    def test_list_with_none_raises_type_error(self):
        """Test: List containing None"""
        with pytest.raises(TypeError, match="All elements must be numbers"):
            find_outlier_median([1, 2, None, 4])

    def test_list_with_mixed_types_raises_type_error(self):
        """Test: List with mixed numeric and non-numeric"""
        with pytest.raises(TypeError):
            find_outlier_median([1, 2, [3], 4])


class TestFindOutlierMedianParameterized:
    """Parameterized tests for find_outlier_median function."""

    @pytest.mark.parametrize(
        "sequence,expected_outlier",
        [
            ([1, 2, 3, 4, 100], 100),
            ([1, 2, 3, 4, -100], -100),
            ([1, 1, 1, 1, 1000], 1000),
            ([10, 20, 30, 40, 200], 200),
            ([-5, -4, -3, -2, -100], -100),
            ([0, 0, 0, 0, 999], 999),
            ([0.1, 0.2, 0.3, 0.4, 9.9], 9.9),
            ([42], 42),
            ([1, 2], 1),
            ([100, 200, 300, 400, 500], 100),
            ([4, 3, 2, 1], 1),
            ([5, 4, 3, 2, 1], 5),
        ],
    )
    def test_parameterized_normal_cases(self, sequence, expected_outlier):
        """Parameterized test for various normal cases"""
        assert find_outlier_median(sequence) == expected_outlier

    @pytest.mark.parametrize(
        "sequence",
        [
            ([1, 2, 3, 4, 5]),
            ([10, 20, 30, 40, 50]),
            ([-10, -5, 0, 5, 10]),
            ([1, 1, 2, 2, 3]),
        ],
    )
    def test_parameterized_no_extreme_outlier(self, sequence):
        """Test sequences without extreme outliers"""
        result = find_outlier_median(sequence)
        assert result in [min(sequence), max(sequence)]

    @pytest.mark.parametrize(
        "invalid_input",
        [
            None,
            "string",
            123,
            3.14,
            {"key": "value"},
        ],
    )
    def test_invalid_input_types(self, invalid_input):
        """Test various invalid input types"""
        with pytest.raises(TypeError):
            find_outlier_median(invalid_input)

    @pytest.mark.parametrize(
        "invalid_sequence",
        [
            [1, 2, "three"],
            [1, None, 3],
            [1, [2], 3],
            [1, {2: 3}, 4],
        ],
    )
    def test_invalid_elements(self, invalid_sequence):
        """Test sequences with invalid elements"""
        with pytest.raises(TypeError):
            find_outlier_median(invalid_sequence)


class TestFindOutlierMedianPerformance:
    """Performance tests for find_outlier_median function."""

    def test_large_sequence_performance(self):
        """Test performance with large sequence"""
        sequence = [1] * 100000 + [1000000]

        start_time = time.time()
        result = find_outlier_median(sequence)
        end_time = time.time()

        assert result == 1000000
        assert end_time - start_time < 0.5

    def test_very_large_numbers_performance(self):
        """Test with very large numbers"""
        sequence = [10**100] * 1000 + [10**1000]
        result = find_outlier_median(sequence)
        assert result == 10**1000


class TestFindOutlierMedianEnhanced:
    """Tests for enhanced version that can return multiple outliers"""

    def test_single_outlier_default(self):
        """Test: Default behavior (single outlier)"""
        result = find_outlier_median_enhanced([1, 2, 3, 4, 100])
        assert result == 100

    def test_multiple_outliers(self):
        """Test: Return multiple outliers"""
        result = find_outlier_median_enhanced([1, 2, 3, 4, 100, 200], outlier_count=2)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] in [100, 200]
        assert result[1] in [100, 200]

    def test_outlier_count_greater_than_sequence(self):
        """Test: Request more outliers than sequence length"""
        result = find_outlier_median_enhanced([1, 2, 3], outlier_count=5)
        assert len(result) == 3

    def test_invalid_outlier_count(self):
        """Test: Invalid outlier count raises error"""
        with pytest.raises(ValueError, match="outlier_count must be positive"):
            find_outlier_median_enhanced([1, 2, 3], outlier_count=0)

        with pytest.raises(ValueError, match="outlier_count must be positive"):
            find_outlier_median_enhanced([1, 2, 3], outlier_count=-1)


class TestGetStatistics:
    """Tests for statistics function"""

    def test_statistics_return_type(self):
        """Test: Statistics returns dictionary with correct keys"""
        stats = get_statistics([1, 2, 3, 4, 100])

        assert isinstance(stats, dict)
        expected_keys = [
            "length",
            "min",
            "max",
            "mean",
            "median",
            "outlier",
            "outlier_distance",
            "max_distance",
            "sorted_sequence",
        ]

        for key in expected_keys:
            assert key in stats

    def test_statistics_values(self):
        """Test: Statistics values are correct"""
        stats = get_statistics([1, 2, 3, 4, 100])

        assert stats["length"] == 5
        assert stats["min"] == 1
        assert stats["max"] == 100
        assert stats["mean"] == 22.0
        assert stats["median"] == 3
        assert stats["outlier"] == 100
        assert stats["outlier_distance"] == 97
        assert stats["max_distance"] == 97

    def test_statistics_empty_sequence(self):
        """Test: Empty sequence raises error"""
        with pytest.raises(ValueError):
            get_statistics([])

    def test_statistics_single_element(self):
        """Test: Single element sequence"""
        stats = get_statistics([42])

        assert stats["length"] == 1
        assert stats["min"] == 42
        assert stats["max"] == 42
        assert stats["mean"] == 42
        assert stats["median"] == 42
        assert stats["outlier"] == 42
        assert stats["outlier_distance"] == 0


class TestTrivialAndEdgeCases:
    """Special focus on trivial and edge cases"""

    def test_trivial_single_element(self):
        """Trivial case: Single element list"""
        assert find_outlier_median([5]) == 5
        assert find_outlier_median([0]) == 0

    def test_trivial_two_elements(self):
        """Trivial case: Two elements"""
        assert find_outlier_median([1, 2]) == 1
        assert find_outlier_median([100, 200]) == 100

    def test_edge_all_identical(self):
        """Edge case: All elements identical"""
        assert find_outlier_median([7, 7, 7, 7, 7]) == 7

    def test_edge_two_distinct_values_only(self):
        """Edge case: Only two distinct values"""
        assert find_outlier_median([1, 1, 1, 2, 2]) == 2
        assert find_outlier_median([-5, -5, 5, 5, 5]) == -5

    def test_edge_alternating_values(self):
        """Edge case: Alternating values"""
        result = find_outlier_median([1, 100, 1, 100, 1])
        assert result == 100

    def test_edge_sorted_ascending(self):
        """Edge case: Already sorted ascending"""
        result = find_outlier_median([1, 2, 3, 4, 5])
        assert result == 1

    def test_edge_sorted_descending(self):
        """Edge case: Already sorted descending"""
        result = find_outlier_median([5, 4, 3, 2, 1])
        assert result == 5
        result = find_outlier_median([4, 3, 2, 1])
        assert result == 1

    def test_edge_zero_values(self):
        """Edge case: Sequence containing zeros"""
        assert find_outlier_median([0, 0, 0, 0, 100]) == 100
        assert find_outlier_median([-100, 0, 0, 0, 0]) == -100

    def test_edge_float_precision(self):
        """Edge case: Floating point precision issues"""
        result = find_outlier_median([0.1, 0.2, 0.3, 0.4, 1e-10])
        # Исправлено: использование 'in' вместо нескольких сравнений
        assert result in (0.4, 1e-10)

    def test_edge_very_small_differences(self):
        """Edge case: Very small differences between values"""
        seq = [1.0000001, 1.0000002, 1.0000003, 1.0000004, 2.0]
        result = find_outlier_median(seq)
        assert result == 2.0

    def test_edge_large_range(self):
        """Edge case: Very large range of values"""
        seq = [-(10**6), -(10**3), 0, 10**3, 10**6]
        result = find_outlier_median(seq)
        assert result == -(10**6)

    def test_edge_negative_zero(self):
        """Edge case: Negative zero vs positive zero"""
        seq = [-0.0, 0.0, 0.0, 0.0, 100]
        result = find_outlier_median(seq)
        assert result == 100

    def test_descending_order_multiple_fixed(self):
        """Test various descending order sequences - FIXED"""
        assert find_outlier_median([4, 3, 2, 1]) == 1
        assert find_outlier_median([5, 4, 3, 2, 1]) == 5
        assert find_outlier_median([6, 5, 4, 3, 2, 1]) == 1
        assert find_outlier_median([7, 6, 5, 4, 3, 2, 1]) == 7


# Educational test to explain all cases
def test_explain_all_behaviors():
    """Educational test to explain all edge cases"""
    print("\n" + "=" * 70)
    print("Complete Explanation of find_outlier_median Function")
    print("=" * 70)

    # Case 1: Odd length ascending
    result = find_outlier_median([1, 2, 3, 4, 5])
    print(f"\n1. [1, 2, 3, 4, 5] -> {result}")
    print("   Sorted: [1,2,3,4,5], median=3")
    print("   Distances: 1:2, 2:1, 3:0, 4:1, 5:2")
    print("   Max distance=2, first element with dist 2 is 1")

    # Case 2: Odd length descending
    result = find_outlier_median([5, 4, 3, 2, 1])
    print(f"\n2. [5, 4, 3, 2, 1] -> {result}")
    print("   Sorted: [1,2,3,4,5], median=3")
    print("   Distances: 5:2, 4:1, 3:0, 2:1, 1:2")
    print("   Max distance=2, first element with dist 2 is 5")

    # Case 3: Even length ascending
    result = find_outlier_median([1, 2, 3, 4])
    print(f"\n3. [1, 2, 3, 4] -> {result}")
    print("   Sorted: [1,2,3,4], median index=2 -> median=3")
    print("   Distances: 1:2, 2:1, 3:0, 4:1")
    print("   Max distance=2, first element with dist 2 is 1")

    # Case 4: Even length descending
    result = find_outlier_median([4, 3, 2, 1])
    print(f"\n4. [4, 3, 2, 1] -> {result}")
    print("   Sorted: [1,2,3,4], median=3")
    print("   Distances: 4:1, 3:0, 2:1, 1:2")
    print("   Max distance=2, first element with dist 2 is 1")

    # Case 5: With clear outlier
    result = find_outlier_median([1, 2, 3, 4, 100])
    print(f"\n5. [1, 2, 3, 4, 100] -> {result}")
    print("   Sorted: [1,2,3,4,100], median=3")
    print("   Distances: 1:2, 2:1, 3:0, 4:1, 100:97")
    print("   Max distance=97, element with dist 97 is 100")


if __name__ == "__main__":
    # Run educational test first
    test_explain_all_behaviors()

    print("\n" + "=" * 70)
    print("Running formal tests...")
    print("=" * 70 + "\n")

    # Run all tests
    exit_code = pytest.main([__file__, "-v", "--tb=short"])

    print("\n" + "=" * 70)
    if exit_code == 0:
        print("✓ All tests passed successfully!")
        print("\n📊 Summary of function behavior:")
        print("   • Sorts the sequence to find median (element at index len//2)")
        print("   • Calculates absolute distances from median")
        print("   • Returns FIRST element in ORIGINAL sequence with maximum distance")
        print("   • For even length, median is the upper middle element")
        print("   • For equal distances, returns first occurrence in original order")
    else:
        print(f"✗ Tests failed with exit code: {exit_code}")
    print("=" * 70)

    input("\nPress Enter to exit...")
    sys.exit(exit_code)
