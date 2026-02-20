nums = [2, 7, 11, 15]
target = 9

for i, num in enumerate(nums):
    for j in range(i + 1, len(nums)):
        if num + nums[j] == target:
            print([i, j])
