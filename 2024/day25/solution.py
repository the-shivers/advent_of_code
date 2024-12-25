with open('input.txt') as f:
    locks = [i.splitlines() for i in f.read().strip().split('\n\n')]

def get_heights(schematic):
    is_lock = schematic[0] == '#####'
    rows = schematic if is_lock else schematic[::-1]
    heights = [sum(1 for row in rows if row[i] == '#') - 1 for i in range(5)]
    return heights, is_lock

locks_keys = [get_heights(lock) for lock in locks]
lock_heights = [h for h, is_lock in locks_keys if is_lock]
key_heights = [h for h, is_lock in locks_keys if not is_lock]

compatible_pairs = 0
for lock in lock_heights:
    for key in key_heights:
        if all(lock[i] + key[i] <= 5 for i in range(5)):
            compatible_pairs += 1
print(compatible_pairs)