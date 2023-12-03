with open('advent_of_code_2023/day3/input.txt') as file:
    lines = file.read().strip().split('\n')
    
parts = []
for y, line in enumerate(lines):
    for x, symbol in enumerate(line):
        if symbol not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']:
            parts.append((x, y))
            
import re
def get_numbers_and_indices(s, y_coord):
    numbers_and_indices = []
    for match in re.finditer(r'\d+', s):
        number = match.group()
        indices = tuple(range(match.start(), match.end()))
        numbers_and_indices.append((number, y_coord, indices))
    return numbers_and_indices

nums = []
for x, line in enumerate(lines):
    nums += get_numbers_and_indices(line, x)
    
def extend_range(tup):
    min_val = min(tup) - 1
    max_val = max(tup) + 1
    return list(range(min_val, max_val + 1))

        
def get_adjacent_coords(num_thing):
    # ('937', 0, (4, 5, 6)) is our input
    y = num_thing[1]
    x_tup = num_thing[2]
    adj_coords = []
    for y in [y-1, y, y+1]:
        for x in extend_range(x_tup):
            adj_coords.append((x, y))
    return adj_coords

# part 1
my_sum = 0
for num in nums:
    adj_coords = get_adjacent_coords(num)
    for i in adj_coords:
        if i in parts:
            my_sum+=int(num[0])
            
# part 2
gears = []
for y, line in enumerate(lines):
    for x, symbol in enumerate(line):
        if symbol in ['*']:
            gears.append((x, y))
            
my_sum = 0
for gear in gears:
    gear_parts = []
    for num in nums:
        adj_coords = get_adjacent_coords(num)
        for i in adj_coords:
            if i == gear:
                gear_parts += [num]
    if len(gear_parts) == 2:
        my_sum += int(gear_parts[0][0]) * int(gear_parts[1][0])
        
        
#### CHATGPT ATTEMPT ####

def sum_part_numbers(schematic):
    rows = schematic.strip().splitlines()
    height, width = len(rows), max(len(row) for row in rows)
    symbols = set("+-*/$%&@#")
    sum_parts = 0

    # Function to extract the number at a specific position
    def extract_number(y, x):
        number = ''
        while x < width and rows[y][x].isdigit():
            number += rows[y][x]
            x += 1
        return int(number) if number else 0

    for y in range(height):
        for x in range(len(rows[y])):
            if rows[y][x].isdigit():
                # Check if the number is adjacent to a symbol
                adjacent_to_symbol = False
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width and rows[ny][nx] in symbols:
                            adjacent_to_symbol = True
                            break
                    if adjacent_to_symbol:
                        break
                if adjacent_to_symbol:
                    sum_parts += extract_number(y, x)
                    # Skip the rest of the digits of the current number
                    while x < width and rows[y][x].isdigit():
                        x += 1

    return sum_parts

# Calculate the sum for the test input
sum_part_numbers('\n'.join(lines))