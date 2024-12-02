from collections import Counter

# input_txt = 'advent_of_code/2024/day1/example.txt'
input_txt = 'advent_of_code/2024/day1/input.txt'
left_list, right_list = [], []
with open(input_txt) as file:
    for line in file:
        l, r = line.split()
        left_list.append(int(l))
        right_list.append(int(r))

# Part One
left_list.sort()
right_list.sort()
total = 0
for i in range(len(left_list)):
    total += abs(left_list[i] - right_list[i])
print(f'Part 1: {total}')

# Part Two
left_counter, right_counter = Counter(left_list), Counter(right_list)
total = 0
for l_key, l_value in left_counter.items():
    if l_key in right_counter:
        total += l_value * l_key * right_counter[l_key]
print(f'Part 2: {total}')