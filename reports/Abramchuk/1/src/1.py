str_list = input("Введите целые числа через пробел: ").split()
nums = []

try:
    for item in str_list:
        nums.append(int(item))

    if len(set(nums)) == 1:
        print("Все числа равны")
    else:
        print("Числа не равны")

except ValueError:
    print("Ошибка: вводить можно только целые числа")
