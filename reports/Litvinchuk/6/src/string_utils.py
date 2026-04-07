def keep(string, pattern):
    if string is None and pattern is None:
        raise TypeError("Both arguments are None")

    if string is None:
        return None

    if string == "":
        return ""

    if pattern is None or pattern == "":
        return ""

    result = ""

    for ch in string:
        if ch in pattern or ch == " ":
            result += ch

    return result