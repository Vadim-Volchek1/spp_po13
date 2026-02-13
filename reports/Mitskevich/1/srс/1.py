arr = input("Введите числа через пробел: ").split()
sizeArr = len(arr)
for i in range(sizeArr):
    for j in range(0, sizeArr-i-1):
        if arr[j] < arr[j+1]:
            temp = arr[j]
            arr[j] = arr[j+1]
            arr [j+1] = temp
print(arr)
