from collections import defaultdict
import heapq

DIRS = {
    '^': (0, -1), 'v': (0, 1), 
    '<': (-1, 0), '>': (1, 0)
}
TURNS = {
    '^': ['<', '>'], '>': ['^', 'v'], 
    'v': ['>', '<'], '<': ['v', '^']
}

def get_costs(grid, start_states, end_pos=None, min_cost=None):
    """Dijkstra's Algorithm from one or more start states."""
    costs = defaultdict(lambda: float('inf'))
    pq = [(0, *state) for state in start_states]
    min_cost = float('inf')
    while pq:
        cost, x, y, facing = heapq.heappop(pq)
        if cost >= costs[x, y, facing] or cost >= min_cost:
            continue
        costs[x, y, facing] = cost
        if end_pos and (x, y) == end_pos:
            min_cost = min(min_cost, cost)
        # Forward move
        dx, dy = DIRS[facing]
        if grid[y+dy][x+dx] != '#':
            heapq.heappush(pq, (cost + 1, x + dx, y + dy, facing))
        # Turn moves
        for new_facing in TURNS[facing]:
            heapq.heappush(pq, (cost + 1000, x, y, new_facing))
    return (costs, min_cost) if end_pos else costs

def solve(grid):
    """
    Solve both parts using bidirectional Dijkstra's algorithm.
    1. get costs from start to all other tiles (incl. min_cost to end for part 1).
    2. get costs from end to all other tiles
    A tile is on optimal path if:
        min_cost_from_start + min_cost_from_end == min_total_cost.
    """
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 'S': start_pos = (x, y)
            elif c == 'E': end_pos = (x, y)
    forward_costs, min_cost = get_costs(grid, [(start_pos[0], start_pos[1], '>')], end_pos)
    print(f"Part 1: {min_cost}")
    backward_costs = get_costs(grid, [(end_pos[0], end_pos[1], d) for d in '<v'], None, min_cost)
    optimal_tiles = set()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != '#':
                for dir1 in '^v<>':
                    for dir2 in '^v<>':
                        if forward_costs[x,y,dir1] + backward_costs[x,y,dir2] == min_cost:
                            optimal_tiles.add((x,y))
                            break               
    print(f"Part 2: {len(optimal_tiles)}")

if __name__ == "__main__":
    grid = [list(line.strip()) for line in open('input.txt')]
    solve(grid)