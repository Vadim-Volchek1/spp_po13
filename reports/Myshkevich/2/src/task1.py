class LimitedSet:
    def __init__(self, capacity, elements=None):
        if capacity <= 0:
            raise ValueError("Мощность должна быть положительной")

        self.capacity = capacity
        self.elements = []

        if elements:
            for elem in elements:
                if len(self.elements) < self.capacity:
                    if float(elem) not in self.elements:
                        self.elements.append(float(elem))

    def __str__(self):
        return f"{{{', '.join(str(x) for x in self.elements)}}}"

    def __eq__(self, other):
        if not isinstance(other, LimitedSet):
            return False
        return set(self.elements) == set(other.elements)

    def contains(self, value):
        return float(value) in self.elements

    def add(self, value):
        try:
            num = float(value)
            if num in self.elements:
                print(f"Элемент {num} уже существует")
            elif len(self.elements) >= self.capacity:
                print(f"Нельзя добавить {num}: достигнута мощность {self.capacity}")
            else:
                self.elements.append(num)
        except ValueError:
            print(f"Ошибка: {value} не является числом")

    def remove(self, value):
        try:
            self.elements.remove(float(value))
        except ValueError:
            print(f"Элемент {value} не найден")
        except (TypeError, ValueError):
            print(f"Ошибка: {value} не является числом")

    def intersection(self, other):
        common = [x for x in self.elements if x in other.elements]
        return LimitedSet(len(common), common)


# Пример использования
set1 = LimitedSet(5, [1.5, 2.7, 3.14, 2.7])  # Дубль 2.7 не добавится
set2 = LimitedSet(5, [2.7, 3.14, 5.5])

print("Множество 1:", set1)
print("Множество 2:", set2)

set1.add(4.8)
print("После добавления 4.8:", set1)

set1.add(4.8)  # Попытка добавить дубль
set1.add(6.6)  # Попытка добавить при полной мощности (если 5 элементов)

print("Содержит 2.7?", set1.contains(2.7))
print("Содержит 9.9?", set1.contains(9.9))

set1.remove(2.7)
print("После удаления 2.7:", set1)

set3 = set1.intersection(set2)
print("Пересечение множеств:", set3)

set4 = LimitedSet(5, [4.8, 1.5, 3.14])
print("Множество 4:", set4)
print("set1 == set4?", set1 == set4)
