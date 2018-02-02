import re

def diversiness(string, len_gain=0.2):
    used_chars = {}
    for i in string:
        if i not in used_chars:
            used_chars[i] = 1
        else:
            used_chars[i] += 1
    return len(used_chars) ** 1.75 / len(string) / 4

def patterns(string):
    length = len(string) // 5
    patterns = 0
    for i in range(len(string)):
        try:
            pattern = r'{}'.format(string[i:i + length])
        except KeyError:
            break
        amount_of_patterns = len(re.findall(pattern, string))
        if amount_of_patterns > 1:
            patterns += 1
    return patterns

print(diversiness('asdasdasdasdasdasdasdasdasdasdasd'))
print(patterns(input()))
