def factorial (number):
    resultFactor = 1
    if number == 0:
        return resultFactor
    for i in range(1, number+1):
        resultFactor*=i
    return resultFactor
value = int (input("Введите число ступенек: "))
valueOfBigStep = value//2
valueOfLittleStep = value%2
result = 0
while valueOfBigStep >= 0:
    result += factorial(valueOfLittleStep+valueOfBigStep)//(factorial(valueOfLittleStep)*(factorial(valueOfBigStep)))
    valueOfBigStep-=1
    valueOfLittleStep +=2
print(f"Результат: {result}")
