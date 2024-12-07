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
# path = simulate(lines)
# print("Part 1:", len(path))

# Part 2
# print("Part 2:", sum(1 for x, y in path if len(simulate(lines, (x, y))) == 0))

# These are our crossing-outcome lookup dictionaries. 


def simulate2(
    array: list[str],
    new_obst: tuple[int, int] = None # For part 2
) -> dict[tuple[int, int], set[str]]:
    x, y, symb = get_guard_pos(lines)
    path = {(x, y): {symb}}
    current = None
    while not is_finished(array, x, y, symb):
        if is_obstructed(array, x, y, symb, new_obst):
            symb = rotate_guard(symb)
            path[(x, y)].add(symb)
            continue
        # print(f"new_obst {new_obst}, {new_obst[0] <= array_center_l}, x = {x}, y={y} array_center_r = {array_center_r}, sym={symb}")
        if new_obst[0] <= array_center_l and x == array_center_l and symb == '>': #entry to right, still on left but on edge
            if (x, y, symb) in lookup:
                if lookup[(x, y, symb)] == 'edge':
                    return path
                elif lookup[(x, y, symb)] == 'cycle':
                    return dict()
                else:
                    x, y, symb = lookup[(x, y, symb)]
                    if (x, y) not in path:
                        path[(x, y)] = set()
                    path[(x, y)].add(symb)
                    continue
            else:
                current = (x, y, symb)
        elif new_obst[0] <= array_center_l and x == array_center_r and symb == '<': # exit to left, still on right but on edge
            if current:
                lookup[current] = (x, y, symb)
                current = None
        x, y, symb = move(x, y, symb)
        if (x, y) in path:
            if symb in path[(x, y)]:
                if current:
                    lookup[current] = 'cycle'
                return dict()  # Exit early if we hit cycle
            path[(x, y)].add(symb)
        else:
            path[(x, y)] = {symb}
    if current:
        lookup[current] = 'edge'
    return path

# print("Part 2:", sum(1 for x, y in path if len(simulate(lines, (x, y))) == 0))
path = simulate(lines)
array_center_l = len(lines[0]) // 2
array_center_r = len(lines[0]) // 2 + 1
lookup = {}
# print(simulate2(lines, (4, 7)))
# print("Part 2:", sum(1 for x, y in path if len(simulate2(lines, (x, y))) == 0))
# print("Part 2:", sum(1 for x, y in path if len(simulate(lines, (x, y))) == 0))
# path = simulate(lines)

lookup = {}
sim1 = set()
sim2 = set()
counter = 0
for x, y in path:
    # lookup = {}
    # if counter % 600 == 0:
    #     print(counter)
    if counter >= 800:
        break
    if len(simulate(lines, (x, y))) == 0:
        sim1.add((x, y))
    if len(simulate2(lines, (x, y))) == 0:
        sim2.add((x, y))
    counter += 1

sim1 - sim2
sim2 - sim1

simulate2(lines, (60, 60))

# array_center_l = len(lines[0]) // 2 - 1
# array_center_r = len(lines[0]) // 2
# a = simulate2(lines, (4, 6))
# a = simulate2(lines, (3, 6))
# a = simulate2(lines, (6, 7))
# a = simulate2(lines, (4, 5))
# lookup = {}
# print("Part 2:", sum(1 for x, y in path if len(simulate2(lines, (x, y))) == 0))


# import timeit

# # Time first version
# time1 = timeit.timeit(
#     lambda: sum(1 for x, y in path if len(simulate(lines, (x, y))) == 0),
#     number=1
# )
# print(f"Original version took {time1:.2f} seconds")

# # Time second version
# time2 = timeit.timeit(
#     lambda: sum(1 for x, y in path if len(simulate2(lines, (x, y))) == 0),
#     number=1
# )
# print(f"New version took {time2:.2f} seconds")