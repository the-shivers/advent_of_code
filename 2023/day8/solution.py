example = 'advent_of_code/2023/day8/example.txt'
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
        return opts[0], directions[1:] + directions[0]
    else:
        return opts[1], directions[1:] + directions[0]
    
counter = 0
start = 'AAA'
while start != 'ZZZ':
    counter += 1
    print(start, directions)
    start, directions = step(directions, mappings, start=start)
    if counter >= 10:
        break