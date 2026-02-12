def rep(start, end, step):
    if start >= end:
        print("Ошибка: start должен быть меньше end")
        return
    if step <= 0:
        print("Ошибка: step должен быть больше 0")
        return

    for i in range(start, end + 1, step):
        print(i, end=" ")

try:
    start = int(input("Введите начало (start): "))
    end = int(input("Введите конец (end): "))
    step = int(input("Введите шаг (step): "))
    rep(start, end, step)
except ValueError:
    print("Ошибка: вводить нужно только целые числа")