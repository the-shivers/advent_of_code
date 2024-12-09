input_txt = 'example.txt'
input_txt = 'input.txt' #6332189866718, 6353648390778
with open(input_txt) as file:
    line = [line.strip() for line in file][0]

def expand(s):
    results = []
    pos, id = 0, 0
    for i in range(0, len(line), 2):
        used = line[i]
        free = line[i + 1] if len(line) > i + 1 else 0
        for i in range(int(used)):
            results.append({"pos": pos, "id": id})
            pos += 1
        if int(used) > 0:
            id += 1
        for i in range(int(free)):
            results.append({"pos": pos, "id": None})
            pos += 1
    return results

def contract(s_expand):
    l, r = 0, len(s_expand) - 1
    while l < r:
        if s_expand[l]['id'] is None:
            if s_expand[r]['id'] is None:
                r -= 1
            else:
                s_expand[l]['id'], s_expand[r]['id'] = s_expand[r]['id'], s_expand[l]['id']
                l += 1
                r -= 1
        else:
            l += 1
    return s_expand

def checksum(s_contract):
    checksum = 0
    for i in s_contract:
        if i['id'] is not None:
            checksum += i['pos'] * i['id']
    return checksum

def contract_pt2(s_expand):
    l1, l2, r1, r2 = 0, 1, len(s_expand) - 1, len(s_expand) - 1
    needed = 0
    free_space = 0
    while r1 > 0:
        if r1 % 500 == 0:
            print(r1)
        if s_expand[r2]['id'] is None:
            r2 -= 1
            r1 -= 1
            continue
        current_id = s_expand[r2]['id']
        while r1 - 1 >= 0 and s_expand[r1 - 1]['id'] == current_id:
            r1 -= 1
        needed = r2 - r1 + 1
        free_space = 0
        l1, l2 = 0, 0
        while l2 < r1:
            if l1 < len(s_expand) and s_expand[l1]['id'] is not None:
                l1 += 1
                l2 += 1
                continue
            while l2 + 1 < len(s_expand) and s_expand[l2 + 1]['id'] is None:
                l2 += 1
            free_space = l2 - l1 + 1
            if free_space >= needed:
                for i in range(needed):
                    s_expand[l1 + i]['id'], s_expand[r2 - i]['id'] = s_expand[r2 - i]['id'], s_expand[l1 + i]['id']
                l1, l2 = l1 + needed, l1 + needed
                break
            else:
                l1, l2 = l2 + 1, l2 + 1
        r2 = r1 - 1
        r1 = r1 - 1 
        needed = 0
        current_id = None
    return s_expand
        
s_expand = expand(line)
s_contract = contract(s_expand)
print("Part 1:", checksum(s_contract)) # 6346871685398

s_expand = expand(line)
s_contract2 = contract_pt2(s_expand) 
print("Part 2:", checksum(s_contract2)) # 6373055193464
