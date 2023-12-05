# input_txt = 'advent_of_code/2022/day4/example.txt'
input_txt = 'advent_of_code/2022/day4/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

def is_contained(line):
    a, b = line.split(',')
    a1, a2 = a.split('-')
    b1, b2 = b.split('-')
    if (int(a1) <= int(b1) and int(a2) >= int(b2)) or (int(b1) <= int(a1) and int(b2) >= int(a2)) :
        return 1
    else:
        return 0
    
print('Pt 1:', sum([is_contained(line) for line in lines])) # 562

def is_overlapping(line):
    a, b = line.split(',')
    a1, a2 = a.split('-')
    b1, b2 = b.split('-')
    if len(set(range(int(a1), int(a2)+1)) & set(range(int(b1), int(b2)+1))) > 0:
        return 1
    else:
        return 0
    
print('Pt 2:', sum([is_overlapping(line) for line in lines])) # 924
