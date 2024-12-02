# input_txt = 'advent_of_code/2024/day1/example.txt'
input_txt = 'advent_of_code/2024/day1/input.txt'

left_list = []
right_list = []

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

print(total)

# Part Two (Could be made faster with binary search)
sim_dict = {}
sim_score = 0
for i in range(len(left_list)):
    if left_list[i] in sim_dict:
        continue
    sim_dict[left_list[i]] = 0
    for j in range(len(right_list)):
        if right_list[j] == left_list[i]:
            sim_dict[left_list[i]] += 1

for l in left_list:
    sim_score += l * sim_dict[l]

print(sim_score)