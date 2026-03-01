numbers = []
items = int(input())
for i in range(items):
    number = int(input())
    numbers.append(number)
print(max(numbers) - min(numbers))
