def index_of_difference(str1, str2):
    if str1 is None or str2 is None:
        raise TypeError("Arguments cannot be None")

    str1 = str1.strip()
    str2 = str2.strip()
    min_length = min(len(str1), len(str2))

    for i in range(min_length):
        if str1[i] != str2[i]:
            return i

    if len(str1) != len(str2):
        return min_length

    return -1
