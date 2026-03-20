def binary_sum():
    a = input().strip()
    b = input().strip()

    num_a = int(a, 2)
    num_b = int(b, 2)

    result = bin(num_a + num_b)[2:]
    print(result)


if __name__ == "__main__":
    binary_sum()
