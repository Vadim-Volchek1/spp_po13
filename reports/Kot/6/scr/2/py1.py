def find_outlier_median(seq):
    # Input validation
    if not isinstance(seq, (list, tuple)):
        raise TypeError("Input must be a list or tuple")

    if len(seq) == 0:
        raise ValueError("Sequence cannot be empty")

    # Check that all elements are numeric
    for item in seq:
        if not isinstance(item, (int, float)):
            raise TypeError(
                f"All elements must be numbers, found {type(item).__name__}"
            )

    # Handle single element case
    if len(seq) == 1:
        return seq[0]

    # Sort the sequence to find median
    seq_sorted = sorted(seq)

    # Find median (middle element for odd length)
    # For even length, we take the lower middle (as in original code)
    median_index = len(seq_sorted) // 2
    median = seq_sorted[median_index]

    # Find outlier: element farthest from median
    outlier = max(seq, key=lambda x: abs(x - median))

    return outlier


def find_outlier_median_enhanced(seq, outlier_count=1):
    if not isinstance(seq, (list, tuple)):
        raise TypeError("Input must be a list or tuple")

    if len(seq) == 0:
        raise ValueError("Sequence cannot be empty")

    if outlier_count < 1:
        raise ValueError("outlier_count must be positive")

    seq_sorted = sorted(seq)
    median_index = len(seq_sorted) // 2
    median = seq_sorted[median_index]

    # Create list of (element, distance) pairs
    distances = [(x, abs(x - median)) for x in seq]

    # Sort by distance and return top outliers
    distances.sort(key=lambda pair: pair[1], reverse=True)
    outliers = [pair[0] for pair in distances[:outlier_count]]

    return outliers if outlier_count > 1 else outliers[0]


def get_statistics(seq):
    if not isinstance(seq, (list, tuple)):
        raise TypeError("Input must be a list or tuple")

    if len(seq) == 0:
        raise ValueError("Sequence cannot be empty")

    seq_sorted = sorted(seq)
    median_index = len(seq_sorted) // 2
    median = seq_sorted[median_index]

    # Find outlier
    outlier = max(seq, key=lambda x: abs(x - median))

    # Calculate statistics
    mean = sum(seq) / len(seq)
    outlier_distance = abs(outlier - median)
    max_distance = max(abs(x - median) for x in seq)

    return {
        "length": len(seq),
        "min": min(seq),
        "max": max(seq),
        "mean": mean,
        "median": median,
        "outlier": outlier,
        "outlier_distance": outlier_distance,
        "max_distance": max_distance,
        "sorted_sequence": seq_sorted,
    }


def main():
    print("Outlier Finder using Median-based Approach")
    print("=" * 50)

    try:
        # Get input from user
        input_str = input("Enter numbers separated by spaces: ").strip()

        if not input_str:
            raise ValueError("No input provided")

        # Parse numbers
        numbers = list(map(float, input_str.split()))

        print("\nArray:", numbers)

        # Find and display outlier
        outlier = find_outlier_median(numbers)
        print("Outlier:", outlier)

        # Display additional statistics
        stats = get_statistics(numbers)
        print("\nStatistics:")
        print("  Median:", stats["median"])
        print("  Mean: {:.2f}".format(stats["mean"]))
        print("  Min:", stats["min"])
        print("  Max:", stats["max"])
        print("  Outlier distance from median:", stats["outlier_distance"])

    except ValueError as err:
        print("Error:", err)
    except TypeError as err:
        print("Error:", err)
    except (OverflowError, ArithmeticError, ZeroDivisionError) as err:
        # Исправление: более конкретные исключения вместо общего Exception
        print("Unexpected error:", err)


if __name__ == "__main__":
    main()
