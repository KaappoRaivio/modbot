def diversiness(string):
    used_chars = {}
    for i in string:
        if i not in used_chars:
            used_chars[i] = 1
        else:
            used_chars[i] += 1
    return len(used_chars) / len(string)
print(diversiness('Rita sanoi juuri että pitää ottaa funktio laskin mukaan ensi tunnin koetta varten jos omistaa semmosen Rita sanoi juuri että pitää ottaa funktio laskin mukaan ensi tunnin koetta varten jos omistaa semmosen'))
    
