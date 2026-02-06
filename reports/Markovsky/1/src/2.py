s = str()
strs = list(map(str, input("Введите строки: ").split()))
if len(strs) > 0:
    strs.sort()
    min_word = min(strs[0], strs[-1])
    max_word = max(strs[0], strs[-1])

    for i in range(len(min_word)):
        if min_word[i] == max_word[i]:
            s += min_word[i]
        else:
            break
print("Cамая длинная общая строка префикса среди списка строк:", s)
