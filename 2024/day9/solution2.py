input_txt = 'example.txt'
input_txt = 'input.txt' #6332189866718, 6353648390778
with open(input_txt) as file:
    line = file.readline().strip()

def expand(s):
    is_file = True
    files, spaces = [], []
    pos, id = 0, 0
    for i in s:
        if is_file:
            if int(i) > 0:  # Only create file entry if length > 0
                files.append({"pos": pos, "id": id, "len": int(i)})
                id += 1
            pos += int(i)
            is_file = False
        else:
            if int(i) > 0:  # Only create space entry if length > 0
                spaces.append({"pos": pos, "id": None, "len": int(i)})
            pos += int(i)
            is_file = True
    return files, spaces

def visualize(files, spaces):
    max_pos = 0
    for f in files:
        max_pos = max(max_pos, f['pos'] + f['len'])
    for s in spaces:
        max_pos = max(max_pos, s['pos'] + s['len'])
    result = ['.'] * max_pos
    for f in files:
        if f['id'] is not None:  # Only show files that haven't been moved
            for i in range(f['len']):
                result[f['pos'] + i] = str(f['id'] % 10)
    for s in spaces:
        if 'content' in s:
            offset = 0
            for f in s['content']:
                for i in range(f['len']):
                    result[s['pos'] + offset] = str(f['id'] % 10)
                    offset += 1
    return ''.join(result)

def contract(files, spaces):
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

def checksum(files, spaces):
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

# Main execution
files, spaces = expand(line)
files, spaces = contract(files, spaces)
print("Part 2:", checksum(files, spaces))