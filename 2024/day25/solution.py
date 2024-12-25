# input_txt = 'example.txt'
input_txt = 'input.txt'
with open(input_txt) as file:
    locks = [i.splitlines() for i in file.read().strip().split('\n\n')]

def raw_lock_to_clean(lock):
    if lock[0] == '#####' and lock[-1] == '.....':
        type = 'lock'
    else:
        type = 'key'
    result = [-1, -1, -1, -1, -1]
    new_lock = lock[:] if type == 'lock' else lock[::-1]
    for row in new_lock:
        for i, char in enumerate(row):
            if char == '#':
                result[i] += 1
    return type, result

def process_raw_locks(raw_locks):
    locks, keys = [], []
    for lock in raw_locks:
        processed = raw_lock_to_clean(lock)
        if processed[0] == 'lock':
            locks.append(processed[1])
        else:
            keys.append(processed[1])
    return locks, keys

locks, keys = process_raw_locks(locks)

print(locks)
print(keys)

# Part 1
pt1 = 0
for l in locks:
    for k in keys:
        if all(l[i] + k[i] <= 5 for i in range(5)):
            pt1 += 1
print(pt1)