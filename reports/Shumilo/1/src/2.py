def hamming_weight(n: int) -> int:
    return bin(n).count("1")

while True:
    user_input = input("Введите положительное целое число: ")
    try:
        n = int(user_input)
        if n < 0:
            print("Ошибка: число должно быть положительным.\n")
            continue
        break
    except ValueError:
        print("Ошибка: нужно ввести целое число.\n")

print("Количество установленных битов:", hamming_weight(n))
