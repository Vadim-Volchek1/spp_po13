def is_palindrome(text: str) -> bool:
    filtered = "".join(char for char in text.lower() if char.isalnum())
    return filtered == filtered[::-1]


def main() -> None:
    user_input = input("Введите строку: ")

    if is_palindrome(user_input):
        print("true")
    else:
        print("false")


if __name__ == "__main__":
    main()
