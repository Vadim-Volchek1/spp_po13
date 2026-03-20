while True:
    raw = input("Введите числа через пробел: ").split()
    nums = []
    ok = True

    for item in raw:
        try:
            nums.append(int(item))
        except ValueError:
            print(f"Ошибка: '{item}' не является целым числом. Попробуйте снова.\n")
            ok = False
            break
    if ok:
        break

dist = {}
for n in nums:
    digits = len(str(abs(n)))
    if digits not in dist:
        dist[digits] = 0
    dist[digits] += 1

print("\nРаспределение по количеству цифр:")
for digits in sorted(dist):
    print(f"{digits}-значных: {dist[digits]}")
