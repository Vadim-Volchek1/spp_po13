# pylint: disable=invalid-name
"""Lab 2, task 1, variant 7.

Limited-capacity set of characters implemented on top of a list.
"""


class LimitedCharSet:
    """Represent a set of unique one-character strings with fixed capacity."""

    def __init__(self, capacity: int, initial: list[str] | None = None) -> None:
        """Initialize the set with capacity and optional initial data."""
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        self._capacity = capacity
        self._items: list[str] = []

        if initial is not None:
            for item in initial:
                self.add(item)

    @property
    def capacity(self) -> int:
        """Return maximum number of elements in the set."""
        return self._capacity

    @capacity.setter
    def capacity(self, new_capacity: int) -> None:
        """Set a new capacity if it is valid for current content."""
        if new_capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        if new_capacity < len(self._items):
            raise ValueError("New capacity cannot be smaller than current set size.")

        self._capacity = new_capacity

    def _validate_symbol(self, symbol: str) -> None:
        """Validate that value is a single character string."""
        if not isinstance(symbol, str):
            raise TypeError("Symbol must be a string.")
        if len(symbol) != 1:
            raise ValueError("Symbol must contain exactly one character.")

    def add(self, symbol: str) -> bool:
        """Add symbol to the set.

        Return True if symbol was added, otherwise False.
        """
        self._validate_symbol(symbol)

        if symbol in self._items:
            return False

        if len(self._items) >= self._capacity:
            raise ValueError("Set capacity exceeded.")

        self._items.append(symbol)
        return True

    def remove(self, symbol: str) -> bool:
        """Remove symbol from the set.

        Return True if symbol existed and was removed, otherwise False.
        """
        self._validate_symbol(symbol)

        if symbol not in self._items:
            return False

        self._items.remove(symbol)
        return True

    def contains(self, symbol: str) -> bool:
        """Return whether the set contains the given symbol."""
        self._validate_symbol(symbol)
        return symbol in self._items

    def get_elements(self) -> list[str]:
        """Return a copy of set elements."""
        return self._items.copy()

    def union(self, other: "LimitedCharSet") -> "LimitedCharSet":
        """Return union of two character sets as a new object."""
        if not isinstance(other, LimitedCharSet):
            raise TypeError("Union is supported only for LimitedCharSet objects.")

        combined_items = self.get_elements()
        for item in other.get_elements():
            if item not in combined_items:
                combined_items.append(item)

        result_capacity = max(self.capacity, other.capacity, len(combined_items))
        return LimitedCharSet(result_capacity, combined_items)

    def __str__(self) -> str:
        """Return human-readable representation of the set."""
        content = ", ".join(self._items)
        return f"LimitedCharSet(capacity={self.capacity}, elements=[{content}])"

    def __eq__(self, other: object) -> bool:
        """Compare two sets by capacity and content."""
        if not isinstance(other, LimitedCharSet):
            return False

        return self.capacity == other.capacity and sorted(self.get_elements()) == sorted(other.get_elements())


def main() -> None:
    """Demonstrate class usage."""
    first_set = LimitedCharSet(5, ["a", "b", "c"])
    second_set = LimitedCharSet(5, ["c", "d"])

    print("First set:", first_set)
    print("Second set:", second_set)

    print("Add 'e' to first set:", first_set.add("e"))
    print("Remove 'b' from first set:", first_set.remove("b"))
    print("Contains 'a':", first_set.contains("a"))
    print("Contains 'z':", first_set.contains("z"))

    united_set = first_set.union(second_set)
    print("Union:", united_set)

    another_set = LimitedCharSet(5, ["a", "c", "e"])
    print("First set == another set:", first_set == another_set)


if __name__ == "__main__":
    main()
