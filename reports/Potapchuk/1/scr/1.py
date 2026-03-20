def unique_numbers():
    n = int(input())
    elements = list(map(int, input().split()))[:n]
    unique_elements = sorted(set(elements))
    print(*unique_elements)


if __name__ == "__main__":
    unique_numbers()
