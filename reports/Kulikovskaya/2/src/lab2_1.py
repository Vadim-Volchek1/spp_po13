import math
from typing import Union

class IsoscelesTriangle:
    def __init__(self, lateral_side: Union[int, float], base: Union[int, float]):
        self._lateral_side = lateral_side
        self._base = base

    @property
    def lateral_side(self) -> Union[int, float]:
        return self._lateral_side

    @lateral_side.setter
    def lateral_side(self, value: Union[int, float]):
        if value <= 0:
            raise ValueError("длина стороны должна быть положительной")
        self._lateral_side = value

    @property
    def base(self) -> Union[int, float]:
        return self._base

    @base.setter
    def base(self, value: Union[int, float]):
        if value <= 0:
            raise ValueError("длина основания должна быть положительной")
        self._base = value

    def is_valid(self) -> bool:
        # Проверка на положительность сторон
        if self._lateral_side <= 0 or self._base <= 0:
            return False

        # Неравенство треугольника для равнобедренного треугольника
        # Две боковые стороны должны быть больше основания
        return 2 * self._lateral_side > self._base

    def perimeter(self) -> Union[int, float]:
        if not self.is_valid():
            raise ValueError("треугольник с такими сторонами не существует")
        return 2 * self._lateral_side + self._base

    def area(self) -> float:
        if not self.is_valid():
            raise ValueError("треугольник с такими сторонами не существует")

        # Вычисление высоты через теорему Пифагора
        # h = sqrt(lateral_side^2 - (base/2)^2)
        half_base = self._base / 2
        height = math.sqrt(self._lateral_side ** 2 - half_base ** 2)

        # Площадь = (основание * высота) / 2
        return (self._base * height) / 2

    def __str__(self) -> str:
        status = "существует" if self.is_valid() else "не существует"
        return (f"равнобедренный треугольник: боковые стороны = {self._lateral_side}, "
                f"основание = {self._base} ({status})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IsoscelesTriangle):
            return NotImplemented

        return (self._lateral_side == other._lateral_side and
                self._base == other._base)


# Создание объектов
print("\n1. Создание треугольников:")
t1 = IsoscelesTriangle(5, 6)  # Валидный треугольник
t2 = IsoscelesTriangle(5, 6)  # Такой же как t1
t3 = IsoscelesTriangle(5, 8)  # Другой треугольник
t4 = IsoscelesTriangle(3, 10)  # Невалидный треугольник (3+3=6 < 10)

print(f"t1 = {t1}")
print(f"t2 = {t2}")
print(f"t3 = {t3}")
print(f"t4 = {t4}")

# Проверка существования
print("\n2. Проверка существования треугольников:")
print(f"t1.is_valid() = {t1.is_valid()}")
print(f"t4.is_valid() = {t4.is_valid()}")

# Вычисление периметра и площади
print("\n3. Периметр и площадь (для валидных треугольников):")
print(f"t1.perimeter() = {t1.perimeter()}")
print(f"t1.area() = {t1.area():.4f}")

print(f"t3.perimeter() = {t3.perimeter()}")
print(f"t3.area() = {t3.area():.4f}")

# Попытка вычислить для невалидного треугольника
print("\n4. Попытка вычислить для невалидного треугольника t4:")
try:
    print(f"t4.perimeter() = {t4.perimeter()}")
except ValueError as e:
    print(f"Ошибка: {e}")

# Сравнение объектов
print("\n5. Сравнение объектов (__eq__):")
print(f"t1 == t2: {t1 == t2} (одинаковые стороны)")
print(f"t1 == t3: {t1 == t3} (разные стороны)")
print(f"t1 == 'string': {t1 == 'string'} (сравнение с не-треугольником)")

# Использование свойств (геттеров и сеттеров)
print("\n6. Работа со свойствами (геттеры и сеттеры):")
print(f"t1.lateral_side = {t1.lateral_side}")
print(f"t1.base = {t1.base}")

# Изменение значений через сеттеры
t1.lateral_side = 7
t1.base = 8
print(f"После изменения: t1 = {t1}")
print(f"Новый периметр: {t1.perimeter()}")
print(f"Новая площадь: {t1.area():.4f}")

# Проверка валидации в сеттере
print("\n7. Проверка валидации в сеттере:")
try:
    t1.lateral_side = -5
except ValueError as e:
    print(f"Ошибка при установке отрицательной стороны: {e}")