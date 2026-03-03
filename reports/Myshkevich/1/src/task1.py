import random

numbers = input("Введите числа через пробел: ").split()
numbers = [int(x) for x in numbers]

random.shuffle(numbers)

print("Числа в случайном порядке:", *numbers)
