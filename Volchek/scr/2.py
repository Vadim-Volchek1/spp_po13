"""Поиск подстроки в строке (аналог str.find)."""
# pylint: disable=invalid-name


def str_str(haystack: str, needle: str) -> int:
    """Возвращает индекс первого вхождения needle в haystack или -1."""
    if not needle:
        return 0
    if len(needle) > len(haystack):
        return -1
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i : i + len(needle)] == needle:
            return i
    return -1
if __name__ == "__main__":
    input_haystack = input("haystack: ").strip()
    input_needle = input("needle: ").strip()
    result = str_str(input_haystack, input_needle)
    print("Output:", result)