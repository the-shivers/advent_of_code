with open('advent_of_code/2022/day1/input.txt') as file:
    lines = [line.strip() for line in file]

max_bag = 0
cur_bag = 0
for line in lines:
    if line:
        cur_bag += int(line)
        max_bag = cur_bag if cur_bag > max_bag else max_bag
    else:
        cur_bag = 0

print('Pt 1:', max_bag)

bag_sums = []
cur_bag = 0
for line in lines:
    if line:
        cur_bag += int(line)
    else:
        bag_sums.append(cur_bag)
        cur_bag = 0
        
print('Pt 2:', sum(sorted(bag_sums, reverse=True)[0:3]))