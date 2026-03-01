class RightTriangle:
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    #  Свойства
    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value <= 0:
            raise ValueError("Сторона должна быть положительным числом.")
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value <= 0:
            raise ValueError("Сторона должна быть положительным числом.")
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        if value <= 0:
            raise ValueError("Сторона должна быть положительным числом.")
        self._c = value

    # Логический метод существования прямоугольного треугольника
    def exists(self) -> bool:
        sides = sorted([self.a, self.b, self.c])
        return abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-9

    # Площадь
    def area(self) -> float:
        if not self.exists():
            raise ValueError("Треугольник не существует.")
        sides = sorted([self.a, self.b, self.c])
        return (sides[0] * sides[1]) / 2

    # Периметр
    def perimeter(self) -> float:
        if not self.exists():
            raise ValueError("Треугольник не существует.")
        return self.a + self.b + self.c

    # Переопределение __str__
    def __str__(self):
        return (f"Прямоугольный треугольник со сторонами: "
                f"a={self.a}, b={self.b}, c={self.c}, "
                f"существует={self.exists()}")

    # Переопределение __eq__
    def __eq__(self, other):
        if not isinstance(other, RightTriangle):
            return False
        return sorted([self.a, self.b, self.c]) == sorted([other.a, other.b, other.c])


t1 = RightTriangle(3, 4, 5)
t2 = RightTriangle(5, 3, 4)
t3 = RightTriangle(2, 3, 4)

print("t1 существует?", t1.exists())
print("t3 существует?", t3.exists())

print("Площадь t1:", t1.area())
print("Периметр t1:", t1.perimeter())


print("t1 == t2 ?", t1 == t2)
print("t1 == t3 ?", t1 == t3)

print(t1)
print(t3)
