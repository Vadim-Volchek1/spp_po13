"""Functions from laboratory work 1."""
import math

def solve_quadratic(a, b, c):
    """Solve a quadratic equation."""
    if a == 0:
        raise ValueError("Not a quadratic equation")
    disc = b**2 - 4*a*c
    if disc < 0:
        return []
    if disc == 0:
        return [-b / (2 * a)]
    return [(-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)]
