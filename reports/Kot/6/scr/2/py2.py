def is_palindrome(x):
    # Input validation
    if not isinstance(x, int):
        raise TypeError("Input must be an integer")

    # Convert to string and check if it reads the same forwards and backwards
    # Note: Negative numbers are not palindromes because of the minus sign
    return str(x) == str(x)[::-1]


def is_palindrome_alternative(x):
    if not isinstance(x, int):
        raise TypeError("Input must be an integer")

    # Negative numbers are not palindromes
    if x < 0:
        return False

    # Single digit numbers are always palindromes
    if x < 10:
        return True

    # Reverse the number mathematically
    original = x
    reversed_num = 0

    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10

    return original == reversed_num


def is_palindrome_enhanced(x, ignore_case=False):
    if not isinstance(x, int):
        raise TypeError("Input must be an integer")

    # For negative numbers, we could optionally ignore minus sign
    if x < 0:
        # Option to consider absolute value
        return str(abs(x)) == str(abs(x))[::-1]

    return str(x) == str(x)[::-1]


def get_palindrome_info(x):
    if not isinstance(x, int):
        raise TypeError("Input must be an integer")

    str_x = str(x)
    reversed_str = str_x[::-1]
    is_pal = str_x == reversed_str

    return {
        "number": x,
        "is_palindrome": is_pal,
        "as_string": str_x,
        "reversed_string": reversed_str,
        "length": len(str_x),
        "absolute_value": abs(x),
        "is_negative": x < 0,
    }


def main():
    print("Palindrome Checker")
    print("=" * 50)

    try:
        # Get input from user
        user_input = input("Enter a number: ").strip()

        if not user_input:
            raise ValueError("No input provided")

        # Convert to integer
        value = int(user_input)

        # Check palindrome
        result = is_palindrome(value)

        print(f"\nNumber: {value}")
        print(f"Is palindrome: {result}")

        # Show additional info
        info = get_palindrome_info(value)
        print(f"\nDetails:")
        print(f"  As string: '{info['as_string']}'")
        print(f"  Reversed: '{info['reversed_string']}'")
        print(f"  Length: {info['length']} digits")

        if not result and value > 0:
            print(
                f"  {value} is not a palindrome because {value} ≠ {info['reversed_string']}"
            )
        elif value < 0:
            print(f"  Negative numbers are not palindromes due to the minus sign")

    except ValueError as e:
        print(f"Error: Invalid input. Please enter a valid integer.")
    except TypeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
