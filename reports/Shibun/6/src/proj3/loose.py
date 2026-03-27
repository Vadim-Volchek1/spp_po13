def loose(str1, remove):
    print("DEBUG:", str1, remove)

    if str1 is None and remove is None:
        raise TypeError("Both arguments cannot be None")

    if str1 is None:
        return None

    if remove is None:
        return str1

    if not isinstance(str1, str):
        raise TypeError("First argument must be a string or None")

    if not isinstance(remove, str):
        raise TypeError("Second argument must be a string or None")

    if str1 == "":
        return ""

    if remove == "":
        return str1

    # Удаляем пробелы
    str1 = str1.replace(" ", "")
    print("AFTER SPACE REMOVAL:", list(str1))

    remove_set = set(remove)
    print("REMOVE SET:", remove_set)

    result = "".join(ch for ch in str1 if ch not in remove_set)
    print("RESULT:", result)
    return result
