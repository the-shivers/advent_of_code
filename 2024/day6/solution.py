with open('input.txt') as file:
    lines = [line.strip() for line in file]

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

# Part 1
path = simulate(lines)
print("Part 1:", len(path))

# Part 2
print("Part 2:", sum(1 for x, y in path if len(simulate(lines, (x, y))) == 0))

# Optimizations:
# "Looking ahead"

array_l, array_r = lines

# These are our crossing-outcome lookup dictionaries. 
array_l, array_r = {}, {}
for i in range(len(lines)):
    array_l[i, len(lines) // ]