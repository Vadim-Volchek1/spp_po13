class CharSet:
    def __init__(self, initial=None):
        self._data = []
        if initial:
            for item in initial:
                if item not in self._data:
                    self._data.append(item)
    def add(self, value):
        if value not in self._data:
            self._data.append(value)
    def remove(self, value):
        if value in self._data:
            self._data.remove(value)
    def contains(self, value):
        return value in self._data
    def intersection(self, other):
        result = CharSet()
        for item in self._data:
            if other.contains(item):
                result.add(item)
        return result
    def __eq__(self, other):
        if not isinstance(other, CharSet):
            return False
        if len(self._data) != len(other._data):
            return False
        for item in self._data:
            if item not in other._data:
                return False
        return True
    def __str__(self):
        return " ".join(self._data)
set1 = CharSet(input().split())
set2 = CharSet(input().split())
intersection_set = set1.intersection(set2)
print(intersection_set)
value = input()
print(set1.contains(value))
set1.add(value)
set1.remove(value)
print(set1 == set2)