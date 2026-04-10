def check_equal(sequence):
    """
    Проверяет, все ли элементы последовательности равны.
    Возвращает "равны", если все равны, иначе "не равны".
    """
    if not sequence:  # пустая последовательность
        return "не равны"

    # Сравниваем каждый элемент с первым
    first = sequence[0]
    for item in sequence:
        if item != first:
            return "не равны"
    return "равны"


# Примеры использования:
if __name__ == "__main__":
    # Ввод последовательности
    nums = list(map(int, input("Введите числа через пробел: ").split()))

    result = check_equal(nums)
    print(result)
