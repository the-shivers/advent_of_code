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
# Could be made faster with dicts and binary search
sim_score = 0
for l in left_list:
    counter = 0
    for r in right_list:
        counter += 1 if l == r else 0
    sim_score += l * counter
print(f'Part 2: {sim_score}')