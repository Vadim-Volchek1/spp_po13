from collections import Counter


def find_majority_element(arr):
    counts = Counter(arr)
    n = len(arr)

    for num, freq in counts.items():
        if freq > n // 2:
            return num

    return None


input_str = input("Введите числа через пробел: ")
nums = list(map(int, input_str.split()))

result = find_majority_element(nums)

if result is not None:
    print(f"Элемент большинства: {result}")
else:
    print("Элемент большинства не найден")
