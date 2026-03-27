def find_longest_common_prefix(strings):
    if not strings:
        return ""

    strings.sort()
    min_word = strings[0]
    max_word = strings[-1]

    prefix = []
    for i, char in enumerate(min_word):
        if i < len(max_word) and char == max_word[i]:
            prefix.append(char)
        else:
            break

    return "".join(prefix)


def parse_strings_input(input_string):
    strings = list(map(str, input_string.split()))
    return strings


def main():
    try:
        input_str = input("Введите строки: ")
        strings = parse_strings_input(input_str)
        prefix = find_longest_common_prefix(strings)
        print(f"Самая длинная общая строка префикса среди списка строк: {prefix}")
    except (ValueError, TypeError) as e:
        print(e)


if __name__ == "__main__":
    main()
