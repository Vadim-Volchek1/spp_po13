def is_palindrome(x):
    return str(x) == str(x)[::-1]


x = int(input("Enter: "))
print(is_palindrome(x))
