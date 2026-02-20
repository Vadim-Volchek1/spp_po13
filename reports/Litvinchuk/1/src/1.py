def rep(start_value: int, end_value: int, step_value: int) -> None:
    if step_value == 0:
        print("Ошибка: шаг не может быть равен 0")
        return

    for number in range(start_value, end_value + 1, step_value):
        print(number, end=" ")

    print()


def main() -> None:
    try:
        start_value = int(input("Введите начало (start): "))
        end_value = int(input("Введите конец (end): "))
        step_value = int(input("Введите шаг (step): "))

        rep(start_value, end_value, step_value)

    except ValueError:
        print("Ошибка: вводить нужно только целые числа")


if __name__ == "__main__":
    main()
