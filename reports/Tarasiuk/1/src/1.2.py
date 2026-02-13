def longestCommonPrefix(strs):
    word = ""
    min_word = min(strs, key=len)
    for i, number in enumerate(min_word):
        for j, value in enumerate(strs):
            if min_word[i] == strs[j][i]:
                continue
            return word
        word += min_word[i]
    return word
