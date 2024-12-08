with open('input.txt') as file:
    lines = []
    row_dict = {}
    col_dict = {}
    for i, line in enumerate(file):
        line = line.strip()
        lines.append(line)
        row_dict[i] = []
        for j, chr in enumerate(line):
            if chr == '#':
                row_dict[i].append(j)
                if j in col_dict:
                    col_dict[j].append(i)
                else:
                    col_dict[j] = [i]
        if not row_dict[i]:
            del row_dict[i]

# Part 1 Functions
def get_guard_pos(array: list[str]) -> tuple[int, int, str]:
    for y, row in enumerate(array):
        for x, chr in enumerate(row):
            if chr in '^><v':
                return x, y, chr

def rotate_guard(symb: str) -> str:
    return '^>v<'[('^>v<'.index(symb) + 1) % 4]

def move(x: int, y: int, symb: str) -> tuple[int, int, str]:
    moves = {
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1),
        '<': (-1, 0)
    }
    dx, dy = moves[symb]
    return x + dx, y + dy, symb

def is_finished(array: list[str], x: int, y: int, symb: str) -> bool:
    nx, ny, _ = move(x, y, symb)
    return not (0 <= nx < len(array[0]) and 0 <= ny < len(array))

def is_obstructed(
    array: list[str],
    x: int,
    y: int,
    symb: str,
    new_obst: tuple[int, int] # For Part 2
) -> bool:
    nx, ny, _ = move(x, y, symb)
    return array[ny][nx] == '#' or (new_obst and (nx, ny) == new_obst)

def simulate(
    array: list[str],
    new_obst: tuple[int, int] = None # For part 2
) -> dict[tuple[int, int], set[str]]:
    x, y, symb = get_guard_pos(lines)
    path = {(x, y): {symb}}
    while not is_finished(array, x, y, symb):
        if is_obstructed(array, x, y, symb, new_obst):
            symb = rotate_guard(symb)
            path[(x, y)].add(symb)
            continue
        x, y, symb = move(x, y, symb)
        if (x, y) in path:
            if symb in path[(x, y)]:
                return dict()  # Exit early if we hit cycle
            path[(x, y)].add(symb)
        path[(x, y)] = {symb}
    return path

# Part 2 Functions
def add_obstruction(x, y, row_dict, col_dict):
    if y in row_dict:
        row_dict[y] = sorted(row_dict[y] + [x])
    else:
        row_dict[y] = [x]
    if x in col_dict:
        col_dict[x] = sorted(col_dict[x] + [y])
    else:
        col_dict[x] = [y]
    return row_dict, col_dict

def remove_obstruction(x, y, row_dict, col_dict):
    row_dict[y].remove(x)
    if not row_dict[y]:  
        del row_dict[y]  
    col_dict[x].remove(y)
    if not col_dict[x]:  
        del col_dict[x]  
    return row_dict, col_dict

def quick_move(x, y, symb, array, row_dict, col_dict):
    if symb == '^':
        if x in col_dict:
            for y_ind in col_dict[x][::-1]:
                if y_ind < y:
                    return 'cont', (x, y_ind + 1, rotate_guard(symb))
        return 'edge', (x, 0, symb)
    elif symb == '>':
        if y in row_dict:
            for x_ind in row_dict[y]:
                if x_ind > x:
                    return 'cont', (x_ind - 1, y, rotate_guard(symb))
        return 'edge', (len(array[0]) - 1, y, symb)
    elif symb == 'v':
        if x in col_dict:
            for y_ind in col_dict[x]:
                if y_ind > y:
                    return 'cont', (x, y_ind - 1, rotate_guard(symb))
        return 'edge', (x, len(array) - 1, symb)
    elif symb == '<':
        if y in row_dict:
            for x_ind in row_dict[y][::-1]:
                if x_ind < x:
                    return 'cont', (x_ind + 1, y, rotate_guard(symb))
        return 'edge', (0, y, symb)

def quick_sim(lines, row_dict, col_dict):
    x, y, symb = get_guard_pos(lines)
    guard_pos_dict = {(x, y): {symb}}
    result = 'cont'
    while result == 'cont':
        result, (x, y, symb) = quick_move(x, y, symb, lines, row_dict, col_dict)
        if (x, y) in guard_pos_dict:
            if symb in guard_pos_dict[(x, y)]:
                result = 'cycle'
            else:
                guard_pos_dict[(x, y)].add(symb)
        else:
            guard_pos_dict[(x, y)] = {symb}
    return result, guard_pos_dict

# Part 1:
path = simulate(lines)
print(len(path))

# Part 2:
cycles = 0
for (x, y) in path:
    row_dict, col_dict = add_obstruction(x, y, row_dict, col_dict)
    result, _ = quick_sim(lines, row_dict, col_dict)
    cycles += 1 if result == 'cycle' else 0
    row_dict, col_dict = remove_obstruction(x, y, row_dict, col_dict)
print(cycles)
