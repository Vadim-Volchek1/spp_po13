import math


class EquilateralTriangle:
    def __init__(self, a: float, b: float, c: float):
        # Инициализация сторон
        self._a = a
        self._b = b
        self._c = c

    # ---------- Свойства ----------

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value

    # ---------- Методы ----------

    def exists(self) -> bool:
        # Проверка существования равностороннего треугольника
        return self._a > 0 and self._a == self._b == self._c

    def perimeter(self) -> float:
        if not self.exists():
            raise ValueError("Треугольник не существует")
        return self._a + self._b + self._c

    def area(self) -> float:
        if not self.exists():
            raise ValueError("Треугольник не существует")
        return (self._a**2 * math.sqrt(3)) / 4

    # ---------- Магические методы ----------

    def __str__(self):
        return f"Равносторонний треугольник со сторонами: {self._a}, {self._b}, {self._c}"

    def __eq__(self, other):
        if not isinstance(other, EquilateralTriangle):
            return NotImplemented
        return self._a == other._a and self._b == other._b and self._c == other._c


# ---------- Точка входа ----------

if __name__ == "__main__":
    t1 = EquilateralTriangle(5, 5, 5)
    t2 = EquilateralTriangle(3, 3, 3)
    t3 = EquilateralTriangle(5, 5, 5)

    print(t1)
    print("Существует:", t1.exists())
    print("Периметр:", t1.perimeter())
    print("Площадь:", round(t1.area(), 2))

    print("t1 == t2:", t1 == t2)
    print("t1 == t3:", t1 == t3)
