# дано целое число numRows, вернуть первые numRows треугольника Паскаля.
# В треугольнике паскаля каждое число является суммой двух чисел, расположенных
# непосредственно над ними
# Input: numRows = 5
# Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]

def pascal_triangle(n):
    triangle = []
    for i in range(n):
        row = [None for _ in range(i + 1)]
        row[0], row[-1] = 1, 1
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle

numRows = int(input("введите количество строк: "))
for row in pascal_triangle(numRows):
    print(row)
