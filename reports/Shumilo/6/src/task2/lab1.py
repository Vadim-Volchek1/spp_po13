def parse_int_list(raw: str) -> list[int]:
    """Преобразует строку в список целых чисел.
       Бросает ValueError, если хотя бы один элемент не int."""
    nums = []
    for item in raw.split():
        try:
            nums.append(int(item))
        except ValueError:
             raise ValueError(f"'{item}' не является целым числом") from exc
    return nums


def digit_distribution(nums: list[int]) -> dict[int, int]:
    """Возвращает распределение чисел по количеству цифр."""
    dist = {}
    for n in nums:
        digits = len(str(abs(n)))
        dist[digits] = dist.get(digits, 0) + 1
    return dist


def hamming_weight(x: int) -> int:
    """Количество установленных битов."""
    if not isinstance(x, int):
        raise TypeError("Аргумент должен быть int")
    if x < 0:
        raise ValueError("Число должно быть неотрицательным")
    return bin(x).count("1")
