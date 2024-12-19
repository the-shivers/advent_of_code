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

print("Part 1:", sum(1 for d in designs if get_combos(d, towels) > 0))
print("Part 2:", sum(get_combos(d, towels) for d in designs))