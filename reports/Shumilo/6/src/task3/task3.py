def indexOfDifference(str1: str, str2: str) -> int:
    # оба None - ошибка
    if str1 is None and str2 is None:
        raise TypeError("Both arguments cannot be None")

    # Если хотя бы один None - тоже ошибка
    if str1 is None or str2 is None:
        raise TypeError("Arguments must be strings")

    # Оба пустые - нет различий
    if str1 == "" and str2 == "":
        return -1

    # Если одна строка пустая, а другая нет - различие в позиции 0
    if str1 == "" or str2 == "":
        return 0

    # Ищем первую позицию, где символы различаются
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return i

    # Если все совпадают, но длины разные - различие в конце короткой строки
    if len(str1) != len(str2):
        return min_len

    # Полное совпадение
    return -1
