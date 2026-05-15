import pytest
from lab1 import calculate_above_average_percentage, pascal_triangle


class TestCalculateAboveAveragePercentage:
    # Тесты для функции calculate_above_average_percentage

    # Тривиальные случаи

    def test_single_element(self):
        # Один элемент — 0% больше среднего
        assert calculate_above_average_percentage([5]) == 0.0

    def test_two_elements_same(self):
        # Два одинаковых элемента — 0% больше среднего
        assert calculate_above_average_percentage([5, 5]) == 0.0

    def test_two_elements_different(self):
        # Два разных элемента — 50% больше среднего
        assert calculate_above_average_percentage([3, 7]) == 50.0

    # Граничные случаи

    def test_all_equal(self):
        # Все элементы равны — 0% больше среднего
        assert calculate_above_average_percentage([5, 5, 5, 5]) == 0.0

    def test_all_above_except_one(self):
        # Все кроме одного больше среднего
        result = calculate_above_average_percentage([1, 10, 10, 10])
        assert result == 75.0

    def test_mixed_positive_negative(self):
        # Смешанные положительные и отрицательные числа
        # [-5, -3, 0, 3, 5], среднее = 0
        # Больше 0: 3, 5 — 2 из 5 = 40%
        assert calculate_above_average_percentage([-5, -3, 0, 3, 5]) == 40.0

    def test_all_negative(self):
        # Все отрицательные числа
        # [-10, -5, -3], среднее = -6
        # Больше -6: -5, -3 — 2 из 3 = 66.67%
        result = calculate_above_average_percentage([-10, -5, -3])
        assert result == 66.67

    def test_large_numbers(self):
        # Большие числа
        result = calculate_above_average_percentage([1000000, 2000000, 3000000])
        # Среднее = 2000000, больше: 3000000 — 1 из 3 = 33.33%
        assert result == 33.33

    def test_with_floats(self):
        # Числа с плавающей точкой
        result = calculate_above_average_percentage([1.5, 2.5, 3.5])
        # Среднее = 2.5, больше: 3.5 — 1 из 3 = 33.33%
        assert result == 33.33

    # Исключительные ситуации

    def test_empty_list_raises_valueerror(self):
        # Пустой список вызывает ValueError
        with pytest.raises(ValueError, match="List cannot be empty"):
            calculate_above_average_percentage([])

    def test_none_raises_typeerror(self):
        # None вызывает TypeError
        with pytest.raises(TypeError, match="Input must be a list"):
            calculate_above_average_percentage(None)

    def test_string_raises_typeerror(self):
        # Строка вызывает TypeError
        with pytest.raises(TypeError, match="Input must be a list"):
            calculate_above_average_percentage("123")

    def test_list_with_string_raises_typeerror(self):
        # Список со строкой вызывает TypeError
        with pytest.raises(TypeError, match="All elements must be numbers"):
            calculate_above_average_percentage([1, 2, "three"])

    def test_list_with_none_raises_typeerror(self):
        # Список с None вызывает TypeError
        with pytest.raises(TypeError, match="All elements must be numbers"):
            calculate_above_average_percentage([1, 2, None])


class TestPascalTriangle:
    # Тесты для функции pascal_triangle

    # Тривиальные случаи

    def test_one_row(self):
        # Одна строка треугольника
        assert pascal_triangle(1) == [[1]]

    def test_two_rows(self):
        # Две строки треугольника
        assert pascal_triangle(2) == [[1], [1, 1]]

    def test_three_rows(self):
        # Три строки треугольника
        assert pascal_triangle(3) == [[1], [1, 1], [1, 2, 1]]

    def test_five_rows(self):
        # Пять строк треугольника
        expected = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
        assert pascal_triangle(5) == expected

    # Граничные случаи

    def test_large_triangle(self):
        # Большой треугольник (10 строк)
        result = pascal_triangle(10)
        assert len(result) == 10
        # Проверяем последнюю строку
        assert result[9] == [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]

    def test_triangle_structure(self):
        # Проверка структуры: границы всегда 1
        result = pascal_triangle(7)
        for row in result:
            assert row[0] == 1
            assert row[-1] == 1

    def test_symmetry(self):
        # Проверка симметрии строк
        result = pascal_triangle(6)
        for row in result:
            assert row == row[::-1]  # Строка равна своему реверсу

    # Исключительные ситуации

    def test_zero_rows_raises_valueerror(self):
        # Ноль строк вызывает ValueError
        with pytest.raises(ValueError, match="num_rows must be positive"):
            pascal_triangle(0)

    def test_negative_rows_raises_valueerror(self):
        # Отрицательное число строк вызывает ValueError
        with pytest.raises(ValueError, match="num_rows must be positive"):
            pascal_triangle(-5)

    def test_float_raises_typeerror(self):
        # Дробное число вызывает TypeError
        with pytest.raises(TypeError, match="num_rows must be an integer"):
            pascal_triangle(5.5)

    def test_string_raises_typeerror(self):
        # Строка вызывает TypeError
        with pytest.raises(TypeError, match="num_rows must be an integer"):
            pascal_triangle("5")

    def test_none_raises_typeerror(self):
        # None вызывает TypeError
        with pytest.raises(TypeError, match="num_rows must be an integer"):
            pascal_triangle(None)
