class CharSet:
    def __init__(self, max_size, initial=None):
        self._max_size = max_size
        self._items = []
        if initial:
            for ch in initial:
                self.add(ch)

    def max_size(self):
        return self._max_size

    def items(self):
        return self._items.copy()

    def add(self, ch):
        if len(ch) == 1 and ch not in self._items and len(self._items) < self._max_size:
            self._items.append(ch)
            self._items.sort()

    def remove(self, ch):
        if ch in self._items:
            self._items.remove(ch)

    def contains(self, ch):
        return ch in self._items

    def union(self, other):
        result = CharSet(self._max_size + other._max_size)
        for ch in self._items:
            result.add(ch)
        for ch in other._items:
            result.add(ch)
        return result

    def display(self):
        print(self._items)

    def __contains__(self, ch):
        return ch in self._items

    def __str__(self):
        return f"CharSet({self._items}, max={self._max_size})"

    def __eq__(self, other):
        return sorted(self._items) == sorted(other._items)


if __name__ == "__main__":
    print("Демонстрация работы CharSet\n")

    s1 = CharSet(3, "abc")
    s2 = CharSet(2, "xy")

    print("Исходные множества:")
    print(f"s1: {s1}")
    print(f"s2: {s2}")

    print("\nДобавление 'd' в s1:")
    s1.add("d")
    s1.display()

    print("\nПопытка добавить 'z' в s2 (превышение мощности):")
    s2.add("z")
    s2.display()

    print("\nУдаление 'b' из s1:")
    s1.remove("b")
    s1.display()

    print(f"\nСодержит ли s1 'a'? {s1.contains('a')}")
    print(f"Содержит ли s1 'b'? {'b' in s1}")

    print("\nОбъединение s1 и s2:")
    s3 = s1.union(s2)
    s3.display()

    s4 = CharSet(3, "ad")
    print(f"\ns1: {s1}")
    print(f"s4: {s4}")
    print(f"s1 == s4? {s1 == s4}")
