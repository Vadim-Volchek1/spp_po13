def repeatStr(pattern: str, repeat: int) -> str:
    if pattern is None:
        raise TypeError("pattern не может быть None")

    if repeat < 0:
        raise ValueError("repeat не может быть отрицательным")

    result = pattern * repeat

    return result
