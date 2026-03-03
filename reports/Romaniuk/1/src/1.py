numbers = input("Введите числа: ").split()
a = b = c = 0
for n in numbers:
    if int(n) < 10 and int(n) > -10:
        a += 1
    elif int(n) < 100 and int(n) > -100:
        b += 1
    elif int(n) < 1000 and int(n) > -1000:
        c += 1
print("Однозначных:", a)
print("Двузначных:", b)
print("Трехзначных:", c)
