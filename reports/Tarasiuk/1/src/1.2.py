def longestCommonPrefix(strs):
    if not strs:
        return ""

    word = ""
    min_word = min(strs, key=len)

    for i, ch in enumerate(min_word):
        for j, _ in enumerate(strs):
            if ch != strs[j][i]:
                return word
        word += ch

    return word
