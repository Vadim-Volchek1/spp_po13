class RightTriangle:
    """Right triangle with side lengths a, b (legs), c (hypotenuse)."""

    def __init__(self, a: float, b: float, c: float):
        """Constructor with initial side length initialization."""
        self._a = float(a)
        self._b = float(b)
        self._c = float(c)

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, value: float) -> None:
        self._a = float(value)

    @property
    def b(self) -> float:
        return self._b

    @b.setter
    def b(self, value: float) -> None:
        self._b = float(value)

    @property
    def c(self) -> float:
        return self._c

    @c.setter
    def c(self, value: float) -> None:
        self._c = float(value)

    def exists(self) -> bool:
        """
        Checks whether such a right triangle exists.
        Conditions: all sides positive, a² + b² = c², triangle inequality.
        """
        if self._a <= 0 or self._b <= 0 or self._c <= 0:
            return False
        legs_sq = self._a**2 + self._b**2
        hyp_sq = self._c**2
        if abs(legs_sq - hyp_sq) > 1e-9:
            return False
        return self._a + self._b > self._c and self._a + self._c > self._b and self._b + self._c > self._a

    def area(self) -> float:
        """Area of the right triangle (half the product of the legs)."""
        if not self.exists():
            raise ValueError("No such triangle exists with these sides")
        return 0.5 * self._a * self._b

    def perimeter(self) -> float:
        """Perimeter of the triangle."""
        if not self.exists():
            raise ValueError("No such triangle exists with these sides")
        return self._a + self._b + self._c

    def __str__(self) -> str:
        return f"RightTriangle(a={self._a}, b={self._b}, c={self._c}, " f"exists={self.exists()})"

    def __eq__(self, other: object) -> bool:
        """Comparison by side lengths (accounting for leg order)."""
        if not isinstance(other, RightTriangle):
            return NotImplemented
        sides_self = sorted([self._a, self._b, self._c])
        sides_other = sorted([other._a, other._b, other._c])
        return sides_self == sides_other


def main() -> None:
    """Input triangle sides, output area, perimeter and comparison."""
    print("Enter the side lengths of the right triangle (a, b — legs, c — hypotenuse):")
    a = float(input("a = "))
    b = float(input("b = "))
    c = float(input("c = "))
    t = RightTriangle(a, b, c)
    print(t)
    if t.exists():
        print(f"Area: {t.area():.4f}")
        print(f"Perimeter: {t.perimeter():.4f}")
    else:
        print("No such right triangle exists.")

    t2 = RightTriangle(3, 4, 5)
    print(f"\nComparison with triangle (3, 4, 5): {t == t2}")


if __name__ == "__main__":
    main()
