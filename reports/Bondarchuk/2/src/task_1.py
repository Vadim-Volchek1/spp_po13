"""
В2
1) Равносторонний треугольник, заданный длинами сторон – Предусмотреть
возможность определения площади и периметра, а также логический метод,
определяющий существует или такой треугольник. Конструктор должен
позволять создавать объекты с начальной инициализацией. Переопределить
метод __eq__, выполняющий сравнение объектов данного типа.
"""

import math
import sys

class Triangular:
    """класс_треугольник"""

    def __init__(self, a = 3, b = 3, c = 3) :
        self.a = a
        self.b = b
        self.c = c

    def print(self) :
        print("a",self.a)
        print("b",self.b)
        print("c",self.c)

    def perimeter(self) :
        return self.a + self.b + self.c

    def area(self) :
        p = self.perimeter()
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def is_exists(self) :
        return self.a + self.b >= self.c and self.a + self.c >= self.b and self.c + self.b >= self.a

    def __eq__(self, other) :
        return self.a == other.a and self.b == other.b and self.c == other.c

if __name__ == '__main__':
    triangular_1 = Triangular(3, 3, 3)
    triangular_2 = Triangular(1, 2, 3)
    triangular_3 = Triangular()

    #"""данные"""
    print("triangular_1 = ")
    triangular_1.print()
    print("triangular_2 = ")
    triangular_2.print()
    print("triangular_3 = ")
    triangular_3.print()

    #"""проверка"""
    if triangular_1.is_exists() :
        print("Треугольник triangular_1 существует")
    else :
        print("Треугольник triangular_1 несуществует")
        sys.exit()
    if triangular_2.is_exists() :
        print("Треугольник triangular_2 существует")
    else :
        print("Треугольник triangular_2 несуществует")
        sys.exit()
    if triangular_3.is_exists():
        print("Треугольник triangular_3 существует")
    else:
        print("Треугольник triangular_3 несуществует")
        sys.exit()

    #сравнение
    if triangular_1 == triangular_2 :
        print("Треугольник triangular_2 = triangular_1")
    else:
        print("Треугольник triangular_2 != triangular_1")
    if triangular_1 == triangular_3 :
        print("Треугольник triangular_2 = triangular_1")
    else:
        print("Треугольник triangular_2 != triangular_1")
