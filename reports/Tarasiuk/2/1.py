class Set:
    def __init__(self, max_size, elements=None):
        if elements is None:
            elements = []
        self.max_size = max_size
        self.elements = list(set(elements))[:max_size]

    def __eq__(self, other):
        return self.elements == other.elements

    def union(self, other):
        new_elements = list(set(self.elements + other.elements))
        new_max = len(new_elements)
        return Set(new_max, new_elements)

    def add(self, item):
        value = int(item)
        if value not in self.elements and len(self.elements) < self.max_size:
            self.elements.append(value)
        elif value in self.elements:
            print(f"Элемент {value} уже состоит в множестве")
        else:
            print(f"Достигнута максимальная мощность {self.max_size}, нельзя добавить больше элементов")
    
    def remove(self, value):
        if value in self.elements:
            self.elements.remove(value)


set1 = Set(6, [1, 2, 3])
set2 = Set(3, [4, 5, 6])

print(set1 == set2)
set3 = set1.union(set2)
print(set3.elements)

set1.add(4)
set1.add(7)
print(set1.elements)
set1.remove(2)
print(set1.elements)