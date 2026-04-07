def rep(start_value: int, end_value: int, step_value: int) -> list[int]:
    if step_value == 0:
        raise ValueError("Step cannot be zero")

    return list(range(start_value, end_value + 1, step_value))


def is_palindrome(text: str) -> bool:
    filtered = "".join(char for char in text.lower() if char.isalnum())
    return filtered == filtered[::-1]