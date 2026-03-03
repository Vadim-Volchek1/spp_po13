class IntegerSet:
    def __init__(self, max_size, elements=None):
        if elements is None:
            elements = []
        self.max_size = max_size
        self.elements = list(set(elements))[:max_size]

    def __str__(self):
        return f"{self.elements}"

    def __repr__(self):
        return f"IntegerSet(max_size={self.max_size}, elements={self.elements})"

    def __eq__(self, other):
        return self.max_size == other.max_size and self.elements == other.elements

    def contains(self, item):
        return item in self.elements

    def union(self, other):
        new_max = max(self.max_size, other.max_size)
        new_elements = list(set(self.elements + other.elements))[:new_max]
        return IntegerSet(new_max, new_elements)

    def add(self, item):
        try:
            num = int(item)
            if num not in self.elements and len(self.elements) < self.max_size:
                self.elements.append(num)
            elif num in self.elements:
                print(f"Элемент {num} уже существует в множестве")
            else:
                print(f"Нельзя добавить {num}: достигнута максимальная мощность {self.max_size}")
        except ValueError:
            print(f"Ошибка: {item} не является целым числом")

    def remove(self, value):
        try:
            self.elements.remove(value)
        except ValueError:
            print(f"Элемент {value} не найден в множестве")


intSet1 = IntegerSet(max_size=5, elements=[6, 6, 2])
intSet2 = IntegerSet(max_size=4)
print(repr(intSet1))
print(repr(intSet2))
intSet2.add(1)
intSet2.add(2)
intSet2.add(3)
intSet2.add(4)
intSet2.add(5)
print("Множество 1:", repr(intSet1))
print("Множество 2:", repr(intSet2))
intSet3 = intSet1.union(intSet2)
print("Объединённое множество 3:", repr(intSet3))
print("Содержит ли множество 3 элемент 8:", intSet3.contains(8))
