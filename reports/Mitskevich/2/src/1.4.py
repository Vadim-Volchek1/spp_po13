from enum import Enum

class Rectangle:
    def __init__(self, a, b):
        if sideB > 0 or sideA > 0:
            self._sideA = a
            self._sideB = b
        else:
            print("Неверный ввод данных, используются значения по умолчанию")
            self._sideA = 5
            self._sideB = 10

    def square(self):
        return self._sideA * self._sideB

    def perimeter(self):
        return 2 * (self._sideA + self._sideB)

    def isKvadrat(self):
        if self._sideA == self._sideB:
            return True
        return False

    def isReal(self):
        if self._sideB <= 0 or self._sideA <= 0:
            return False
        return True

    def __eq__(self, other):
        if self.square() == other.square():
            return True
        return False

class Menu(Enum):
    CREATE = 1
    SQUARE = 2
    PERIM = 3
    IS_KVAD = 4
    IS_REAL = 5
    EQ = 6
    EXT = 7

print("МЕНЮ")
print(f"{Menu.CREATE.value}) Создать прямоугольник")
print(f"{Menu.SQUARE.value}) Посчитать площадь")
print(f"{Menu.PERIM.value}) Посчитать периметр")
print(f"{Menu.IS_KVAD.value}) Квадрат ли это")
print(f"{Menu.IS_REAL.value}) Может ли он существовать")
print(f"{Menu.EQ.value}) Сравнить площади")
print(f"{Menu.EXT.value}) Выход")

rect = None
rect_2 = None

while True:
    chouse = int(input("\nСделайте выбор "))
    match chouse:
        case Menu.CREATE.value:
            sideA = int(input("Введите сторону А"))
            sideB = int(input("Введите сторону В"))
            rect = Rectangle(sideA, sideB)

        case Menu.SQUARE.value:
            if rect:
                print(f"Площадь = {rect.square()}")
            else:
                print("Сначала создайте прямоугольник!")

        case Menu.PERIM.value:
            if rect:
                print(f"Периметр = {rect.perimeter()}")
            else:
                print("Сначала создайте прямоугольник!")

        case Menu.IS_KVAD.value:
            if rect:
                print(f"Квадрат ли это? {rect.isKvadrat()}")
            else:
                print("Сначала создайте прямоугольник!")

        case Menu.IS_REAL.value:
            if rect:
                print(f"Может ли существовать? {rect.isReal()}")
            else:
                print("Сначала создайте прямоугольник!")

        case Menu.EQ.value:
            if rect:
                side_a = int(input("Введите сторону А для второго прямоугольника: "))
                side_b = int(input("Введите сторону В для второго прямоугольника: "))
                rect_2 = Rectangle(side_a, side_b)
                print(f"Равны ли площади? {rect == rect_2}")
            else:
                print("Сначала создайте первый прямоугольник!")

        case Menu.EXT.value:
            print("ДО СВИДАНИЯ!")
            break

        case _:
            print("Неверный выбор! Попробуйте снова.")
