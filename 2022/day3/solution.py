input_txt = 'advent_of_code/2022/day3/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]
    
def scr(l):
    return ord(l) - ord('a') + 1 if l.islower() else ord(l) - ord('A') + 27

# Part 1
sum([scr((set(i[:len(i)//2]) & set(i[len(i)//2:])).pop()) for i in lines]) # 7875

# Part 2
summ = 0
for i in range(0, 300, 3):
    set1, set2, set3 = [set(lines[i+j]) for j in range(3)]
    summ += scr((set1 & set2 & set3).pop())
summ # 2479
