def uniq_numbers(param):
    uniq = set(param)
    return uniq

N = int(input("Введите кол-во чисел: "))
numbers = []

for i in range(N):
    num = int(input(f"Введите число {i+1}: "))
    numbers.append(num)

print("Уникальные числа: ", uniq_numbers(numbers))
