class RealSet:

    def __init__(self, elements=None):
        self._data = []
        if elements:
            for element in elements:
                self.add(element)

    @property
    def size(self):
        return len(self._data)

    @property
    def data(self):
        return self._data.copy()

    def __str__(self):
        return "{" + ", ".join([str(round(x, 2)) for x in self._data]) + "}"

    def __eq__(self, other):
        if not isinstance(other, RealSet):
            return False
        return sorted(self._data) == sorted(other.data)

    def contains(self, x):
        try:
            return float(x) in self._data
        except ValueError:
            return False

    def add(self, x):
        try:
            num = float(x)
            if num not in self._data:
                self._data.append(num)
            else:
                print(f"Элемент {num} уже существует")
        except ValueError:
            print("Ошибка: нужно вещественное число")

    def remove(self, x):
        try:
            self._data.remove(float(x))
        except ValueError:
            print(f"Элемент {x} не найден")

    def union(self, other_set):
        if not isinstance(other_set, RealSet):
            print("Ошибка: аргумент должен быть объектом RealSet")
            return None

        new_data = list(set(self._data + other_set.data))
        return RealSet(new_data)


print("=== Множество вещественных чисел (переменной мощности) ===\n")

set_a = RealSet([1.5, 2.3, 3.7])
set_b = RealSet([2.3, 4.1])

print(f"A: {set_a}, размер: {set_a.size}")
print(f"B: {set_b}, размер: {set_b.size}")

print("\n=== Тест добавления ===")
set_a.add(5.5)
set_a.add(1.5)
set_a.add(7.8)
set_a.add(9.2)
print(f"A после добавлений: {set_a}, размер: {set_a.size}")

print("\n=== Тест contains ===")
print(f"2.3 в A? {set_a.contains(2.3)}")
print(f"10.0 в A? {set_a.contains(10.0)}")

print("\n=== Тест объединения ===")
set_c = set_a.union(set_b)
print(f"A: {set_a}")
print(f"B: {set_b}")
print(f"Объединение A ∪ B: {set_c}, размер: {set_c.size}")

print("\n=== Тест удаления ===")
set_a.remove(2.3)
print(f"A после удаления 2.3: {set_a}, размер: {set_a.size}")
set_a.remove(15.0)

print("\n=== Тест __eq__ ===")
set_d = RealSet([1.5, 3.7, 5.5, 7.8, 9.2])
print(f"A: {set_a}")
print(f"D: {set_d}")
print(f"A == D? {set_a == set_d}")

set_e = RealSet([1.5, 5.5, 3.7, 7.8, 9.2])
print(f"E: {set_e}")
print(f"A == E? {set_a == set_e}")

print("\n=== Тест с пустым множеством ===")
empty_set = RealSet()
print(f"Пустое множество: {empty_set}, размер: {empty_set.size}")
empty_set.add(10.5)
print(f"После добавления: {empty_set}, размер: {empty_set.size}")

print("\n=== Тест с отрицательными числами ===")
set_f = RealSet([-1.5, -2.7, 0, 3.14])
print(f"F: {set_f}, размер: {set_f.size}")
