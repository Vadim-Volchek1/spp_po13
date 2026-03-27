import pytest


def factorial(number):

    # Добавляем проверку на отрицательные числа
    if number < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел")

    resultFactor = 1
    if number == 0:
        return resultFactor
    for i in range(1, number + 1):
        resultFactor *= i
    return resultFactor


def countVar(value):

    if not isinstance(value, int):
        raise TypeError("Аргумент должен быть целым числом")

    if value < 0:
        raise ValueError("Аргумент не может быть отрицательным")

    valueOfBigStep = value // 2
    valueOfLittleStep = value % 2
    result = 0

    while valueOfBigStep >= 0:
        result += factorial(valueOfLittleStep + valueOfBigStep) // (
            factorial(valueOfLittleStep) * factorial(valueOfBigStep)
        )
        valueOfBigStep -= 1
        valueOfLittleStep += 2

    return result


# ТЕСТЫ ДЛЯ ФАКТОРИАЛА


@pytest.mark.parametrize(
    "number, expected", [(0, 1), (1, 1), (2, 2), (5, 120), (10, 3628800)]
)
def test_factorial(number, expected):
    """Тестирование факториала"""
    result_test = factorial(number)
    assert result_test == expected


def test_factorial_negative():
    """Тест: факториал отрицательного числа"""
    with pytest.raises(
        ValueError, match="Факториал определён только для неотрицательных чисел"
    ):
        factorial(-1)

    with pytest.raises(ValueError):
        factorial(-5)


# ТЕСТЫ ДЛЯ COUNTVAR


@pytest.mark.parametrize(
    "number, expected", [(0, 1), (1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (10, 89)]
)
def test_countVar(number, expected):
    """Тестирование countVar"""
    result_test = countVar(number)
    assert result_test == expected


def test_countVar_negative():
    """Тест: отрицательное значение"""
    with pytest.raises(ValueError, match="Аргумент не может быть отрицательным"):
        countVar(-1)

    with pytest.raises(ValueError):
        countVar(-5)


def test_countVar_non_integer():
    """Тест: передача не целого числа"""
    with pytest.raises(TypeError, match="Аргумент должен быть целым числом"):
        countVar(3.5)

    with pytest.raises(TypeError):
        countVar("5")

    with pytest.raises(TypeError):
        countVar([5])
