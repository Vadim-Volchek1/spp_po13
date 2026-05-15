import math


class IsoscelesTriangle:
    def __init__(self, a, b, c):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Стороны должны быть положительными")
        if not (math.isclose(a, b) or math.isclose(a, c) or math.isclose(b, c)):
            raise ValueError("Треугольник должен быть равнобедренным")
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Треугольник не существует")
        self.a, self.b, self.c = a, b, c

    def exists(self):
        return True

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        p = self.perimeter() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def __str__(self):
        return (
            f"Равнобедренный треугольник: {self.a:.2f}, {self.b:.2f}, {self.c:.2f}\n"
            f"Периметр: {self.perimeter():.2f}, Площадь: {self.area():.2f}"
        )

    def __eq__(self, other):
        if not isinstance(other, IsoscelesTriangle):
            return False
        return sorted([self.a, self.b, self.c]) == sorted([other.a, other.b, other.c])


# Демонстрация
if __name__ == "__main__":
    t1 = IsoscelesTriangle(5, 5, 3)
    t2 = IsoscelesTriangle(3, 5, 5)
    t3 = IsoscelesTriangle(6, 6, 6)

    print("Треугольник 1:")
    print(t1)
    print(f"Существует: {t1.exists()}\n")

    print("Треугольник 2:")
    print(t2)
    print(f"Существует: {t2.exists()}\n")

    print(f"Треугольник 1 == Треугольник 2: {t1 == t2}")
    print(f"Треугольник 1 == Треугольник 3: {t1 == t3}")

    # Проверка ошибок
    try:
        IsoscelesTriangle(3, 4, 5)  # Не равнобедренный
    except ValueError as e:
        print(f"\nОшибка: {e}")

    try:
        IsoscelesTriangle(1, 1, 3)  # Не существует
    except ValueError as e:
        print(f"Ошибка: {e}")
