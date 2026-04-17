def is_equal(nums):
    if not all(isinstance(x, int) for x in nums):
        raise TypeError("Все элементы должны быть целыми числами")
    if len(nums) == 0:
        return True

    return len(set(nums)) == 1


def return_indexes_sum(nums, target):
    if not all(isinstance(x, int) for x in nums) or not isinstance(target, int):
        raise TypeError("Все элементы списка и target должны быть целыми числами")

    for i, num in enumerate(nums):
        for j in range(i + 1, len(nums)):
            if num + nums[j] == target:
                return [i, j]

    return None
