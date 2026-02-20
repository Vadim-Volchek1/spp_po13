"""Модуль для вычисления моды введённой последовательности чисел."""
# pylint: disable=invalid-name
import sys
from collections import Counter

numbers = []
s = input("Количество чисел: ").strip()
if not s:
    print("Нужно ввести число.")
    sys.exit()
items = int(s)
for i in range(items):
    s = input(f"Число {i + 1}: ")
    if not s.strip():
        print("Пропуск — введите число.")
        sys.exit()
    numbers.append(int(s))
counts = Counter(numbers)
if not counts:
    print("Мода: последовательность пуста.")
else:
    max_count = max(counts.values())
    modes = [x for x, c in counts.items() if c == max_count]
    if max_count == 1 and len(modes) == len(numbers):
        print("Мода: нет (все числа встречаются по одному разу).")
    else:
        print("Мода:", ", ".join(map(str, sorted(modes))))
