# для последовательности из N целых чисел реализовать обработку
# вывод процента чисел, которые больше среднего значения

N = list(map(int, input("Введите последовательность чисел: ").split()))
averageN = sum(N) / len (N) if N else 0
count_above_average = 0
for num in N:
    if num > averageN:
        count_above_average += 1
percentage = round(((count_above_average / len(N)) * 100), 2)
print (f"percent= {percentage}%")
