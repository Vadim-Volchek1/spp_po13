def is_palindrome(s):
    filtered = ""
    for char in s.lower():
        if char.isalnum():
            filtered += char
    return filtered == filtered[::-1]
s = input("Введите строку: ")

if is_palindrome(s):
    print("true")
else:
    print("false")