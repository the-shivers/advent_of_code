def get_full_number(x, y):
    """Take digit coords; get full number's leftmost coords and value
    Input: 3, 8
    Output: {(2, 8): 72}"""
    l_coord = r_coord = x
    while l_coord > MINX and lines[y][l_coord - 1].isdigit():
        l_coord -= 1
    while r_coord < MAXX and lines[y][r_coord + 1].isdigit():
        r_coord += 1
    return {(l_coord, y): int(lines[y][l_coord:r_coord + 1])}

def analyze_part(part):
    """Take part, explore around it, update to include adjacent numbers
    Input: {'symbol': '#', 'x': 2, 'y': 4, 'nums': {}}
    Update: {'symbol': '#', 'x': 2, 'y': 4, 'nums': {(0, 4): 28}}"""
    for y in range(max(part['y'] - 1, MINY), min(part['y'] + 2, MAXY + 1)):
        for x in range(max(part['x'] - 1, MINX), min(part['x'] + 2, MAXX + 1)):
            if lines[y][x].isdigit():
                part['nums'].update(get_full_number(x, y))

with open('advent_of_code_2023/day3/input.txt') as file:
    lines = [line.strip() for line in file]

NON_SYMBOLS = set('1234567890.')
MINX, MINY = 0, 0
MAXX, MAXY = len(lines[0]) - 1, len(lines) - 1

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