from math import sqrt

class IsoscelesTriangle:
    def __init__(self, side, base):
        self._side = side
        self._base = base

    # Гетеры, сеторы
    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if value <= 0:
            raise ValueError("Сторона должна быть больше 0")
        self._side = value

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        if value <= 0:
            raise ValueError("Основание должно быть больше 0")
        self._base = value

    # Методы
    def get_perimeter(self):
        return 2 * self._side + self._base

    def get_square(self):
        h = sqrt(self._side**2 - (self._base / 2)**2)
        return 0.5 * self._base * h

    def is_exists(self):
        return self._side > 0 and self._base > 0 and (2 * self._side > self._base)

    # Переопределение
    def __str__(self):
        return f"Равнобедренный треугольник: боковые стороны = {self._side}, основание = {self._base}"

    def __eq__(self, other):
        if not isinstance(other, IsoscelesTriangle):
            return False
        return self._side == other._side and self._base == other._base


t1 = IsoscelesTriangle(20, 10)
print(t1)
print(f"Существует: {t1.is_exists()}")
print(f"Периметр: {t1.get_perimeter()}")
print(f"Площадь: {t1.get_square():.2f}")

t2 = IsoscelesTriangle(20, 10)
print(f"Треугольники равны? {t1 == t2}")
