# pylint: disable=invalid-name

"""Лабораторная работа 1, задание 2, вариант 7.

Программа принимает большое целое число в виде списка цифр,
увеличивает его на единицу и выводит результат.
"""

from typing import List


def parse_digits(text: str) -> List[int]:
    """Преобразует строку с цифрами в список целых цифр."""
    parts = text.split()
    if not parts:
        raise ValueError("Пустой ввод")

    digits = [int(item) for item in parts]

    if any(digit < 0 or digit > 9 for digit in digits):
        raise ValueError("Есть нецифровые значения")

    if len(digits) > 1 and digits[0] == 0:
        raise ValueError("Число не должно содержать ведущих нулей")

    return digits


def plus_one(digits: List[int]) -> List[int]:
    """Увеличивает число, представленное списком цифр, на единицу."""
    result = digits[:]
    index = len(result) - 1
    carry = 1

    while index >= 0 and carry > 0:
        new_value = result[index] + carry
        result[index] = new_value % 10
        carry = new_value // 10
        index -= 1

    if carry > 0:
        result.insert(0, carry)

    return result


def main() -> None:
    """Точка входа в программу."""
    raw_input_data = input("Введите цифры числа через пробел: ")

    try:
        digits = parse_digits(raw_input_data)
    except ValueError:
        print("Ошибка: введите цифры от 0 до 9 без ведущих нулей.")
        return

    updated_digits = plus_one(digits)
    print(f"Результат: {updated_digits}")


if __name__ == "__main__":
    main()
