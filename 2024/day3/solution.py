import re

# input_txt = 'advent_of_code/2024/day3/example.txt'
input_txt = 'advent_of_code/2024/day3/input.txt'
with open(input_txt) as file:
    input_str = ''.join([line.strip() for line in file])

# Part 1
def get_products(s: str) -> int:
    regex = re.compile(r'mul\((\d+),(\d+)\)')
    matches = regex.findall(s)
    sum = 0
    for pair in matches:
        sum += int(pair[0]) * int(pair[1])
    return sum

print(f'Part 1: {get_products(input_str)}')

# Part 2
total = 0
remaining = input_str[:]
while True:
    parts_list = remaining.split("don't()", 1)
    if len(parts_list) == 1:
        total += get_products(parts_list[0])
        break
    good, bad = parts_list
    total += get_products(good)
    parts_list = bad.split("do()", 1)
    if len(parts_list) == 1:
        break
    bad, remaining = parts_list

print(f'Part 2: {total}')