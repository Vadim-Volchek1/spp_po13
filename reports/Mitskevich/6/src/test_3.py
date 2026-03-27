import pytest


def indexOfDifference(str1, str2):
    # Проверка на None
    if str1 is None or str2 is None:
        raise ValueError("Нельзя использовать none значения")

    # Если обе строки пустые
    if str1 == "" and str2 == "":
        return -1

    # Если одна из строк пустая, а другая нет
    if str1 == "" or str2 == "":
        return 0
    i = 0
    while i < len(str1) and i < len(str2):
        if str1[i] == str2[i]:
            return i

    return -1


# ТЕСТЫ


@pytest.mark.parametrize(
    "str_1, str_2, result",
    [
        ("", "", -1),
        ("", "abc", 0),
        ("abc", "", 0),
        ("abc", "abc", -1),
        ("ab", "abxyz", 2),
        ("abcde", "abxyz", 2),
        ("abcde", "xyz", 0),
        ("qwertyuiopasdfghjkl", "qwertyuiopasdfghjkl", -1),
    ],
)
def test_indexOfDifference(str_1, str_2, result):

    result_test = indexOfDifference(str_1, str_2)
    assert result_test == result


def test_indexOfDifference_none():

    with pytest.raises(ValueError, match="Нельзя использовать none значения"):
        indexOfDifference(None, None)
