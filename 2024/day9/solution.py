input_txt = 'example.txt'
input_txt = 'input.txt' 
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

def expand2(s):
    is_file = True
    files, spaces = [], []
    pos, id = 0, 0
    for i in s:
        if is_file:
            files.append({"pos": pos, "id": id, "len": int(i)})
            id += 1
            pos += int(i)
            is_file = False
        else:
            # if int(i) > 0:  # Only create space entry if length > 0
            spaces.append({"pos": pos, "id": None, "len": int(i)})
            pos += int(i)
            is_file = True
    return files, spaces

def contract2(files, spaces):
    for file in reversed(files):
        for space in spaces:
            if space['len'] >= file['len'] and space['pos'] < file['pos']:
                if 'content' not in space:
                    space['content'] = []
                space['content'].append({"id": file['id'], 'len': file['len']})
                space['len'] -= file['len']
                file['id'] = None
                break
    return files, spaces

def checksum2(files, spaces):
    total = 0
    for f in files:
        if f['id'] is not None:
            total += sum(f['id'] * (f['pos'] + i) for i in range(f['len']))
    for s in spaces:
        if 'content' in s:
            offset = 0
            for f in s['content']:
                for i in range(f['len']):
                    total += f['id'] * (s['pos'] + offset)
                    offset += 1
    return total

s_expand = expand(line)
s_contract = contract(s_expand)
print("Part 1:", checksum(s_contract)) # 6346871685398

files, spaces = expand2(line)
files, spaces = contract2(files, spaces)
print("Part 2:", checksum2(files, spaces)) # 6373055193464
