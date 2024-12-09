from collections import defaultdict

def find_guard(grid):
    for y, row in enumerate(grid):
        for x, symb in enumerate(row):
            if symb in '^>v<':
                return x, y, symb

def move(x, y, symb, grid, _, __): # _ & __ for compatibility with quick_move
    """Advance guard, step-by-step, through the grid."""
    moves = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
    next_x, next_y = x + moves[symb][0], y + moves[symb][1]
    if grid[next_y][next_x] == '#':
        return x, y, '^>v<'[('^>v<'.index(symb) + 1) % 4]
    return next_x, next_y, symb

def get_obst_maps(grid):
    """Get list of obstruction indices for each row/col for quick_move."""
    row_obs, col_obs = defaultdict(list), defaultdict(list)
    for y, row in enumerate(grid):
        for x, symb in enumerate(row):
            if symb == '#':
                row_obs[y].append(x)
                col_obs[x].append(y)
    return row_obs, col_obs
    
def quick_move(x, y, symb, grid, row_obs, col_obs):
    """
    Instead of going step-by-step, jump to the index before the
    next obstacle in the path (if it exists) else jump to edge.
    """
    width, height = len(grid[0]), len(grid)
    if symb == '^':
        if (ny := next((y2 for y2 in reversed(col_obs[x]) if y2 < y), None)) is not None:
            return x, ny + 1, '>'
        return x, 0, symb
    if symb == '>':
        if (nx := next((x2 for x2 in row_obs[y] if x2 > x), None)) is not None:
            return nx - 1, y, 'v'
        return width - 1, y, symb
    if symb == 'v':
        if (ny := next((y2 for y2 in col_obs[x] if y2 > y), None)) is not None:
            return x, ny - 1, '<'
        return x, height - 1, symb
    if symb == '<':
        if (nx := next((x2 for x2 in reversed(row_obs[y]) if x2 < x), None)) is not None:
            return nx + 1, y, '^'
        return 0, y, symb

def simulate(grid, x, y, symb, row_obs, col_obs, move_func):
    """Advance guard until he hits an edge or cycle."""
    path = defaultdict(list)
    path[(x, y)].append(symb)
    width, height = len(grid[0]), len(grid)
    while True:
        x, y, symb = move_func(x, y, symb, grid, row_obs, col_obs)
        if symb in path[(x, y)]:
            return 'cycle', path
        path[(x, y)].append(symb)
        if x in (0, width - 1) or y in (0, height - 1):
            return 'edge', path

def get_prior_pos(x, y, symb):
    prior_dict = {
        '^': (x, y + 1, '^'), '>': (x - 1, y, '>'), 
        'v': (x, y - 1, 'v'), '<': (x + 1, y, '<')
    }
    return prior_dict[symb]

def solve(filename):
    with open(filename) as f:
        grid = [line.strip() for line in f]
    x, y, symb = find_guard(grid)
    row_obs, col_obs = get_obst_maps(grid)
    _, path = simulate(grid, x, y, symb, row_obs, col_obs, move)
    part1 = len(path)
    part2 = 0
    for (x, y), symbs in path.items():
        simulation = simulate(
            grid, *get_prior_pos(x, y, symbs[0]), 
            {**row_obs, y: sorted(row_obs[y] + [x])},
            {**col_obs, x: sorted(col_obs[x] + [y])},
            quick_move
        )
        part2 += simulation[0] == 'cycle'
    print(f"Part 1: {part1}\nPart 2: {part2}")

if __name__ == '__main__':
    solve('input.txt')