def calculate_range(numbers):
    if not numbers:
        raise ValueError("Последовательность пустая")

    min_val = min(numbers)
    max_val = max(numbers)
    return min_val, max_val, max_val - min_val


def parse_numbers_input(input_string):
    try:
        numbers = list(map(int, input_string.split()))
        return numbers
    except ValueError as e:
        raise ValueError("Последовательность некорректна - введите целые числа!") from e


def main():
    try:
        input_str = input("Введите последовательность целых чисел: ")
        numbers = parse_numbers_input(input_str)
        min_val, max_val, range_val = calculate_range(numbers)
        print(f"Размах последовательности: {max_val} - {min_val} = {range_val}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
