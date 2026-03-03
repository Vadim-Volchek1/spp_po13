while True:
    text = input("Input: ")
    if text == "":
        break

    number = int(text)
    binary = bin(number)

    count = 0
    for symbol in binary:
        if symbol == "1":
            count = count + 1

    print("Output:", count)
    print()
