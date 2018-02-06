import re, inspect


class Viesti(object):
    def __init__(self, string):
        self.string = string
        self.length = len(string)
        self.methods = inspect.getmembers(self, predicate=inspect.ismethod)

    def diversiness(self, len_gain=0.2):
        used_chars = {}
        for i in self.string:
            if i not in used_chars:
                used_chars[i] = 1
            else:
                used_chars[i] += 1
        return len(used_chars) ** 1.75 / self.length / 4

    def patterns(self):
        pattern_length = self.length // 5
        patterns = 0
        for i in range(self.length):
            try:
                pattern = r'{}'.format(self.string[i:i + pattern_length])
            except KeyError:
                break
            amount_of_patterns = len(re.findall(pattern, self.string))
            if amount_of_patterns > 1:
                patterns += 1
        return patterns

    def amountOfPunctuationCharacters(self):
        pattern = r'[^A-Za-zÅåÄäÖö0-9 ]'
        return len(re.findall(pattern, self.string)) / self.length

viesti = Viesti(input())

for i in range(len(viesti.methods)): # Iteroidaan luokan Viesti metodeissa.
    if viesti.methods[i][0] is not '__init__':
        print(viesti.methods[i][1]())
