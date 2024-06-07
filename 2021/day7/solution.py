filename = 'input.txt'
with open(filename) as raw_input:
    crabs = [int(i) for i in raw_input.readline().split(',')]
    crabs.sort()

def median(sorted_list):
    if len(sorted_list) % 2 == 0:
        return sorted_list[len(sorted_list) // 2 - 1 : len(sorted_list) // 2 + 1]
    else:
        return [sorted_list[len(sorted_list) // 2]]
    
med = median(crabs)[0]
res = 0
for crab in crabs:
    res += abs(med-crab)

print(res)

pos_dict = {}
for i in range(1, 1001):
    res = 0
    for crab in crabs: 
        t = abs(crab - i)
        res += (t ** 2 + t) // 2
    pos_dict[i] =  res

min(pos_dict.values())
