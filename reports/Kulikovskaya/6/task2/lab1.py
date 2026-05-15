def calculate_above_average_percentage(numbers):
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")

    if len(numbers) == 0:
        raise ValueError("List cannot be empty")

    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("All elements must be numbers")

    average = sum(numbers) / len(numbers)
    count_above_average = sum(1 for num in numbers if num > average)
    percentage = round(((count_above_average / len(numbers)) * 100), 2)
    return percentage


def pascal_triangle(num_rows):
    if not isinstance(num_rows, int):
        raise TypeError("num_rows must be an integer")

    if num_rows <= 0:
        raise ValueError("num_rows must be positive")

    triangle = []
    for i in range(num_rows):
        row = [None for _ in range(i + 1)]
        row[0], row[-1] = 1, 1
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle
