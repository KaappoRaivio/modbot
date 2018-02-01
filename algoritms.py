def diversiness(string):
    used_chars = {}
    for i in string:
        if i not in used_chars:
            used_chars[i] = 1
        else:
            used_chars[i] += 1
    return len(used_chars) / len(string)
print(diversiness(input()))
