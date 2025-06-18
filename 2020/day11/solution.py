from collections import Counter

# input_txt = 'example.txt'
input_txt = 'input.txt'
with open(input_txt) as file:
    lines = [list(line.strip()) for line in file]

h, w = len(lines), len(lines[0])

def print_lines(grid):
    for row in grid:
        print(''.join(row))

def count_neighbors(grid, row, col):
    neighbors = {'L': 0, '.': 0, '#': 0}
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx == 0 and dy == 0) \
            or row + dy < 0 or row + dy >= h \
            or col + dx < 0 or col + dx >= w:
                continue
            neighbors[grid[row + dy][col + dx]] += 1
    neighbors['self'] = grid[row][col]
    return neighbors

def count_neighbors2(grid, row, col):
    neighbors = {'L': 0, '.': 0, '#': 0}
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx == 0 and dy == 0):
                continue
            i = 1
            # print('symbolself', grid[row][col], 'actual row', row, 'actual col', col, 'trow', row + (i * dy), 'tcol', col + (i * dx), grid[row + (i * dy)][col + (i * dx)])
            while (
                row + (i * dy) >= 0 and row + (i * dy) < h \
                and col + (i * dx) >= 0 and col + (i * dx) < w
            ):
                # print('in while i', i, 'trow', row + (i * dy), 'tcol', col + (i * dx), grid[row + (i * dy)][col + (i * dx)])
                if grid[row + (i * dy)][col + (i * dx)] == '.':
                    i += 1
                    continue
                else:
                    # print('hit something', grid[row + (i * dy)][col + (i * dx)])
                    neighbors[grid[row + (i * dy)][col + (i * dx)]] += 1
                    break
    neighbors['self'] = grid[row][col]
    return neighbors

def update_from_neighbors(d, k=4):
    """Takes output from count_neighbors, returns new symbol"""
    if d['self'] == 'L' and d['#'] == 0:
        return '#'
    if d['self'] == '#' and d['#'] >= k:
        return 'L'
    return d['self']

def simulate(grid, cn_func, k=4):
    """One pass to get all needed info, another to update."""
    plan = {} # (x, y) or (col, row) with char and neighbor info
    for y in range(h):
        for x in range(w):
            neighbors = cn_func(grid, y, x, )
            plan[(x, y)] = update_from_neighbors(neighbors, k)
    for y in range(h):
        for x in range(w):
            grid[y][x] = plan[(x, y)]

def summarize_grid(grid):
    full_str = ''
    for row in grid:
        for char in row:
            full_str += char
    return Counter(full_str)

# Simulate Part 1
streak = highscore = last_highscore = 0
counter = summarize_grid(lines)
while streak < 4:
    simulate(lines, count_neighbors, k=4)
    counter = summarize_grid(lines)
    if counter['#'] == highscore:
        streak += 1
    else:
        streak = 1
    highscore, last_highscore = counter['#'], highscore

print("Part 1:", highscore)

# Part 2 just needs a few function modifications.
with open(input_txt) as file:
    lines = [list(line.strip()) for line in file]
streak = highscore = last_highscore = 0
counter = summarize_grid(lines)
while streak < 4:
    simulate(lines, count_neighbors2, 5)
    counter = summarize_grid(lines)
    print(counter)
    if counter['#'] == highscore:
        streak += 1
    else:
        streak = 1
    highscore, last_highscore = counter['#'], highscore

print("Part 2:", highscore)



