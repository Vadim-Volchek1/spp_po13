"""Levenshtein distance calculation module."""

def levenshteinDistance(s, t):
    """Calculate the Levenshtein distance between two strings."""
    if s is None and t is None:
        raise TypeError("Both arguments are None")
    if s is None or t is None:
        return -1

    n, m = len(s), len(t)
    if n == 0:
        return m
    if m == 0:
        return n

    matrix = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        matrix[i][0] = i
    for j in range(m + 1):
        matrix[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s[i-1] == t[j-1] else 1
            matrix[i][j] = min(
                matrix[i-1][j] + 1,
                matrix[i][j-1] + 1,
                matrix[i-1][j-1] + cost
            )

    return matrix[n][m]
