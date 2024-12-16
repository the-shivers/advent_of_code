import time

import heapq
from collections import defaultdict

DIRS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
TURNS = {'^': ['<', '>'], '>': ['^', 'v'], 'v': ['>', '<'], '<': ['v', '^']}

def get_pos(grid, char):
    for y, line in enumerate(grid):
        for x, chr in enumerate(line):
            if chr == char:
                return (x, y)

def part1(start_pos):
    pq = [(0, start_pos[0], start_pos[1], '>')]
    visited = set()
    while pq:
        cost, x, y, facing = heapq.heappop(pq)
        if (x, y, facing) in visited:
            continue
        visited.add((x, y, facing))
        if grid[y][x] == 'E':
            return cost
        # Forward
        dx, dy = DIRS[facing]
        if grid[y+dy][x+dx] != '#':
            if (x + dx, y + dy, facing) not in visited:
                heapq.heappush(pq, (cost + 1, x + dx, y + dy, facing))
        # Turns
        for new_facing in TURNS[facing]:
            if (x, y, new_facing) not in visited:
                heapq.heappush(pq, (cost + 1000, x, y, new_facing))

def get_costs(grid, start_pos, facing):
    costs = defaultdict(lambda: float('inf'))
    pq = [(0, start_pos[0], start_pos[1], facing)]
    while pq:
        cost, x, y, facing = heapq.heappop(pq)
        if cost >= costs[(x, y, facing)]:
            continue
        costs[(x, y, facing)] = cost
        # Forward
        dx, dy = DIRS[facing]
        new_x, new_y = x + dx, y + dy
        if grid[y+dy][x+dx] != '#':
            heapq.heappush(pq, (cost + 1, new_x, new_y, facing))
        # Turns
        for new_facing in TURNS[facing]:
            heapq.heappush(pq, (cost + 1000, x, y, new_facing))  
    return costs

def solve_part2(grid, min_cost):
    start_pos = get_pos(grid, 'S')
    forward_costs = get_costs(grid, start_pos, '>')
    end_pos = get_pos(grid, 'E')
    backward_costs_v = get_costs(grid, end_pos, 'v')  # For paths ending with '^'
    backward_costs_l = get_costs(grid, end_pos, '<')  # For paths ending with '>'
    optimal_tiles = set()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != '#':
                for dir1 in '^v<>':
                    for costs in [backward_costs_v, backward_costs_l]:
                        for dir2 in '^v<>':
                            if forward_costs[(x, y, dir1)] + costs[(x, y, dir2)] == min_cost:
                                optimal_tiles.add((x, y))
    return len(optimal_tiles)

def qp(s, elapsed):
    """Quick print nice looking time text."""
    if elapsed < 0.001:
        print(f"{s}: Execution time: {elapsed*1000000:.2f} microseconds")
    elif elapsed < 1:
        print(f"{s}: Execution time: {elapsed*1000:.2f} milliseconds")
    else:
        print(f"{s}: Execution time: {elapsed:.4f} seconds")

# Fast Parts 1 and 2
start = time.time()
input_txt = 'input.txt'
with open(input_txt) as file:
    grid = [list(line.strip()) for line in file]
start_pos = get_pos(grid, 'S')
pt1_cost = part1(start_pos)
pt1_end = time.time()
print("Part 1:", pt1_cost)
print("Part 2:", solve_part2(grid, pt1_cost))
pt2_end = time.time()
qp("Part 1 Fast", pt1_end - start)
qp("Part 2 Fast", pt2_end - pt1_end)

# Concise Parts 1 and 2
def solve(grid):
    start_pos = get_pos(grid, 'S')
    pq = [(0, start_pos[0], start_pos[1], '>', {(start_pos[0], start_pos[1])})]
    visited = {}  # (x, y, facing) -> cost
    min_cost = float('inf')
    optimal_tiles = set()
    while pq:
        cost, x, y, facing, path = heapq.heappop(pq)
        if cost > min_cost: continue
        state = (x, y, facing)
        # Only skip if we've seen this state with a better cost
        if state in visited and visited[state] < cost:
            continue
        visited[state] = cost
        # Finish
        if grid[y][x] == 'E':
            if cost < min_cost:
                min_cost = cost
                optimal_tiles = path
            elif cost == min_cost:
                optimal_tiles.update(path)
            continue
        # Forward
        dx, dy = DIRS[facing]
        if grid[y+dy][x+dx] != '#':
            heapq.heappush(pq, (cost + 1, x + dx, y + dy, facing, path | {(x + dx, y + dy)}))
        # Turns
        for new_facing in TURNS[facing]:
            heapq.heappush(pq, (cost + 1000, x, y, new_facing, path.copy()))
    return min_cost, len(optimal_tiles)

start = time.time()
grid = [list(line.strip()) for line in open('input.txt')]
p1, p2 = solve(grid)
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")

qp("Parts 1 and 2 Concise:",time.time() - start)