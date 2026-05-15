def repeat(pattern, count):
    """
    Строит строку из указанного паттерна, повторённого заданное количество раз.

    Спецификация:
        repeat("e", 0) = ""
        repeat("e", 3) = "eee"
        repeat("ABC", 2) = "ABCABC"
        repeat("e", -2) = ValueError
        repeat(None, 1) = TypeError
    """
    # Проверка типов
    if pattern is None:
        raise TypeError("pattern must be a string")
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")
    if not isinstance(count, int):
        raise TypeError("repeat must be an integer")

    # Проверка на отрицательное значение
    if count < 0:
        raise ValueError("repeat cannot be negative")

    # Повторение паттерна
    return pattern * count
