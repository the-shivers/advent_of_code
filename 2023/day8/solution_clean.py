example = 'advent_of_code/2023/day8/example.txt'
example2 = 'advent_of_code/2023/day8/example2.txt'
input_txt = 'advent_of_code/2023/day8/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

directions = lines[0]
mappings = lines[2:]

def step(directions, mappings, start='AAA'): 
    mapping = ''
    for i in mappings:
        if i[0:3] == start:
            mapping = i
            break
    opts = [i.strip() for i in mapping.split('(')[1].split(')')[0].split(',')]
    if directions[0] == 'L':
        return opts[0]
    else:
        return opts[1]
    
counter = 0
start = 'AAA'
while start != 'ZZZ':
    counter += 1
    start = step(directions, mappings, start=start)
    directions = directions[1:] + directions[0]
print('Part 1:', counter) # 17141

# Part 2
starts = {}
for i in mappings:
    if i[2] == 'A':
        starts[i[0:3]]= {'current': i[0:3], 'z_list': []}
    
counter = 0
finish_count = 0
while finish_count != len(starts):
    counter += 1
    for start, startdict in starts.items():
        result = step(directions, mappings, start=startdict['current'])
        starts[start]['current'] = result
        if result[-1] == 'Z':
            starts[start]['z_list'].append(counter)
    directions = directions[1:] + directions[0]
    if counter >= 100000:
        break
    
import math
from functools import reduce

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

pt2 = reduce(lcm, [val['z_list'][0] for key, val in starts.items()])
print('Part 2:', pt2) # 10818234074807
