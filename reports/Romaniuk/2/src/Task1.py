class RealSet:
    def __init__(self, max_size=10, elements=None):
        self._max_size = max_size
        self._data = []
        if elements:
            for e in elements:
                self.add(e)

    def get_size(self):
        return len(self._data)

    def get_max_size(self):
        return self._max_size

    def set_max_size(self, value):
        if value < len(self._data):
            print("Ошибка: новый размер меньше текущего количества элементов")
        else:
            self._max_size = value

    def __str__(self):
        return "{" + ", ".join([str(round(x, 2)) for x in self._data]) + "}"

    def __eq__(self, other):
        if not isinstance(other, RealSet):
            return False
        return sorted(self._data) == sorted(other._data)

    def contains(self, x):
        return x in self._data

    def add(self, x):
        try:
            num = float(x)
            if num not in self._data:
                if len(self._data) < self._max_size:
                    self._data.append(num)
                else:
                    print(f"Ошибка: достигнут максимум ({self._max_size} элементов)")
            else:
                print(f"Элемент {num} уже существует")
        except:
            print("Ошибка: нужно вещественное число")

    def remove(self, x):
        try:
            self._data.remove(float(x))
        except:
            print(f"Элемент {x} не найден")

    def union(self, other):
        new_max = max(self._max_size, other._max_size)
        new_data = list(set(self._data + other._data))
        return RealSet(new_max, new_data[:new_max])


# пример
a = RealSet(5, [1.5, 2.3, 3.7])
b = RealSet(3, [2.3, 4.1])
print(f"A: {a}, размер: {a.get_size()}/{a.get_max_size()}")
a.add(5.5)
a.add(1.5)  # уже есть
print(f"A после добавлений: {a}")
print(f"2.3 в A? {a.contains(2.3)}")
c = a.union(b)
print(f"Объединение A и B: {c}")
a.remove(2.3)
print(f"A после удаления: {a}")
print(f"A == RealSet(5, [1.5, 3.7, 5.5])? {a == RealSet(5, [1.5, 3.7, 5.5])}")
