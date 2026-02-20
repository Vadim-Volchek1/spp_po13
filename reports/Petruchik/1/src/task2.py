""""Всем привет, это моя вторая программа(меня  заставил это написать pylint)"""
digits = list(map(int, input().split()))

for i in range(len(digits)-1, -1, -1):
    if digits[i] < 9:
        digits[i] += 1
        print(digits)
        break
    digits[i] = 0
else:
    digits = [1] + digits
    print(digits)
