import math

class EquilateralTriangle:
    def __init__(self, side: float):
        self.side = side

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if value <= 0:
            raise ValueError("Длина стороны должна быть положительным числом.")
        self._side = float(value)

    def exists(self) -> bool:
        return self.side > 0 # ну этого хватит, он же равносторонний

    @property
    def perimeter(self) -> float:
        return 3 * self.side

    @property
    def area(self) -> float:
        return (math.sqrt(3) / 4) * (self.side ** 2)

    def __eq__(self, other) -> bool:
        if not isinstance(other, EquilateralTriangle):
            return False
        return self.side == other.side

    def __str__(self):
        return (f"Равносторонний треугольник: сторона = {self.side}, "
                f"периметр = {self.perimeter:.2f}, площадь = {self.area:.2f}")

t1 = EquilateralTriangle(5)
t2 = EquilateralTriangle(5)
t3 = EquilateralTriangle(7)

print(t1)
print("t1 == t2:", t1 == t2)
print("t1 == t3:", t1 == t3)
print("Существует ли t1:", t1.exists())
