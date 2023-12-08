example = 'advent_of_code/2022/day7/example.txt'
input_txt = 'advent_of_code/2022/day7/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

def return_to_root():
    return ['/']

def move_in(cursor, dir_name):
    cursor.append(dir_name)
    return cursor

def move_out(cursor):
    return cursor[:-1]

def add_to_struct(struct, cursor, name, size):
    current_dict = struct
    for i in cursor:
        current_dict = current_dict[i]
    current_dict[name] = size

def sum_nested_dict(d):
    sum_dict = {}
    def recurse(sub_dict, current_path):
        if isinstance(sub_dict, dict):
            total = 0
            for key, value in sub_dict.items():
                next_path = f"{current_path}/{key}" if current_path else key
                total += recurse(value, next_path)
            if current_path:
                sum_dict[current_path] = total
            return total
        else:
            return sub_dict
    recurse(d, '')
    return sum_dict
        

cursor = ['/']
struct = {'/': {}}
files_only = {}

for line in lines:
    print(line)
    command = line.split()
    if command[0] == '$':
        if command[1] == 'cd' and command[2] == '/':
            cursor = return_to_root()
        elif command[1] == 'cd' and command[2] == '..':
            cursor = move_out(cursor)
        elif command[1] == 'cd':
            cursor = move_in(cursor, command[2])
    elif command[0].isnumeric():
        add_to_struct(struct, cursor, command[1], int(command[0]))
        files_only['/'.join(cursor)[1:] + '/' + command[1]] = int(command[0])
    elif command[0] == 'dir':
        add_to_struct(struct, cursor, command[1], {})

sums = sum_nested_dict(struct)

# Part 1 (1391690)
print('Part 1:', sum(val for key, val in sums.items() if val <= 100000))

# Part 2 (5469168)
current_space_occupied = sums['']
free_space = 70000000 - current_space_occupied
space_needed = 30000000 - free_space

min_viable_dir_name = ''
min_viable_dir_size = 9999999999999
for key, value in sums.items():
    if value >= space_needed and value < min_viable_dir_size:
        min_viable_dir_name = key
        min_viable_dir_size = value
print('Part 2:', min_viable_dir_size)
