# input_txt = 'advent_of_code/2022/day5/example.txt'
input_txt = 'advent_of_code/2022/day5/input.txt'
with open(input_txt) as file:
    lines = [line for line in file]

def get_initial_stacks(lines):
    stacks = dict(zip(range(1, 10), [[] for i in range(9)]))
    indices = [1 + 4 * i for i in range(9)]
    for row, line in enumerate(lines):
        if line.strip() == '':
            break
        for index, char in enumerate(line):
            if index in indices and char.isalpha():
                stacks[1 + indices.index(index)].insert(0, char)
    commands = lines[row + 1:]
    return stacks, commands

def adjust_stacks(stacks, line):
    nums = [int(i) for i in line.strip().split() if i.isnumeric()]
    for i in range(nums[0]):
        stacks[nums[2]].append(stacks[nums[1]].pop())
        
def adjust_stacks2(stacks, line):
    nums = [int(i) for i in line.strip().split() if i.isnumeric()]
    in_transit = stacks[nums[1]][-nums[0]:]
    stacks[nums[1]] = stacks[nums[1]][0:len(stacks[nums[1]]) - nums[0]]
    stacks[nums[2]] += in_transit
    
# PT 1
stacks, commands = get_initial_stacks(lines)
for command in commands:
    adjust_stacks(stacks, command)
print("".join([stacks[i][-1] for i in range(1, 10)])) # FRDSQRRCD

# PT 2
stacks, commands = get_initial_stacks(lines)
for command in commands:
    adjust_stacks2(stacks, command)
print("".join([stacks[i][-1] for i in range(1, 10)])) # HRFTQVWNN