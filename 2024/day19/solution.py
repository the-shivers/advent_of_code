from functools import lru_cache 

@lru_cache(maxsize = None) 
def get_combos(s, towels):
    combos = 1 if s in towels else 0
    for i in range(0, len(s)):
        if s[:i] in towels:
            combos += get_combos(s[i:], towels)
    return combos

with open('input.txt') as file:
    lines = [line.strip() for line in file]
    towels = frozenset(lines[0].split(', '))
    designs = lines[2:]

pt1 = pt2 = 0
for design in designs:
    pt1 += 1 if get_combos(design, towels) > 0 else 0
    pt2 += get_combos(design, towels)
print(f"Part 1: {pt1}\nPart 2: {pt2}")