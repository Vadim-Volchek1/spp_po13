def repeat(pattern, count):
    if pattern is None:
        raise TypeError("pattern cannot be None")

    if count < 0:
        raise ValueError("repeat must be non-negative")

    return pattern * count
    