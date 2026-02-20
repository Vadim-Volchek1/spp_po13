""""Всем привет, моя первая программа на питоне(меня заставил это написать pylint)"""
arr = list(map(int, input().split()))

for n in range(len(arr)-1):
    for j in range(len(arr)-n-1):
        if arr[j+1]>arr[j]:
            temp = arr[j+1]
            arr[j+1] = arr[j]
            arr[j] = temp

if len(arr)%2 != 0:
    print(f"медиана последовательности: {arr[int(len(arr)/2)]}")
else:
    print(f"медиана последовательности: {(arr[int(len(arr) / 2)] + arr[int((len(arr) / 2)-1)])/2}")
