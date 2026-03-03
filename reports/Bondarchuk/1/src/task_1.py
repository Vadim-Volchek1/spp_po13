"""1.2)"""

def product(nums) :
    """произведение"""
    if len(nums) == 0:
        return  0
    prod = 1
    for num in nums:
        prod*=num
    return prod

if __name__ == '__main__':
    mas = list(map(int,(input("mas: ").split())))
    print("max: ",max(mas))
    print("min: ",min(mas))
    print("sum: ",sum(mas))
    print("prod: ",product(mas))
