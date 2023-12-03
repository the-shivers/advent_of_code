def get_full_number(x, y):
    l_coord = r_coord = x
    while l_coord > MIN_X and lines[y][l_coord - 1].isdigit():
        l_coord -= 1
    while r_coord < MAX_X and lines[y][r_coord + 1].isdigit():
        r_coord += 1
    return {(l_coord, y): int(lines[y][l_coord:r_coord + 1])}

def analyze_part(part):
    for x in range(max(part['x'] - 1, MIN_X), min(part['x'] + 2, MAX_X + 1)):
        for y in range(max(part['y'] - 1, MIN_Y), min(part['y'] + 2, MAX_Y + 1)):
            if lines[y][x].isdigit():
                part['nums'].update(get_full_number(x, y))

with open('advent_of_code_2023/day3/input.txt') as file:
    lines = [line.strip() for line in file]

NON_SYMBOLS = set('1234567890.')
MIN_X, MIN_Y = 0, 0
MAX_X, MAX_Y = len(lines[0]) - 1, len(lines) - 1

unique_part_nums = {}
gears = []

for y, line in enumerate(lines):
    for x, symbol in enumerate(line):
        if symbol not in NON_SYMBOLS:
            part = {'symbol': symbol, 'x': x, 'y': y, 'nums': {}}
            analyze_part(part)
            unique_part_nums.update(part['nums'])
            if part['symbol'] == '*' and len(part['nums']) == 2:
                gears.append(part)

# Part 1
print(sum(unique_part_nums.values()))

# Part 2
print(sum(a * b for gear in gears for a, b in [tuple(gear['nums'].values())]))