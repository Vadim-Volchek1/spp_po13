import pytest


def bubbleSort(arr):
    sizeArr = len(arr)
    for i in range(sizeArr):
        for j in range(0, sizeArr - i - 1):
            if arr[j] < arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr


@pytest.mark.parametrize(
    "arr, result_arr",
    [
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([5, 4, 3, 2, 1], [5, 4, 3, 2, 1]),
        ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1]),
        ([-1, -2, -3, -4, 0], [0, -1, -2, -3, -4]),
        ([5, 5, 5, 5, 5], [5, 5, 5, 5, 5]),
        ([], []),
        ([2], [2]),
        ([1, 2], [2, 1]),
        ([-5, 5], [5, -5]),
    ],
)
def test_bubbleSort(arr, result_arr):
    result_test = bubbleSort(arr)
    assert result_test == result_arr


# ИСКЛЮЧИТЕЛЬНЫЕ


def test_bubbleSort_with_none():
    """Тест: передача None вместо массива"""
    with pytest.raises(TypeError) as exc_info:
        bubbleSort(None)
    assert "object of type 'NoneType' has no len()" in str(exc_info.value)


def test_bubbleSort_with_non_list():
    """Тест: передача не списка"""
    with pytest.raises(TypeError):
        bubbleSort(42)

    with pytest.raises(TypeError):
        bubbleSort("string")

    with pytest.raises(TypeError):
        bubbleSort(3.14)
