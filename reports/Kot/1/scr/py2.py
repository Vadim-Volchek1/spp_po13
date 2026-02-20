def is_palindrome(x):
    return str(x) == str(x)[::-1]
value = int(input("Enter: "))
print(is_palindrome(value))
