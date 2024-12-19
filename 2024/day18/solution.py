import heapq

W, H = 71, 71
DIRS = {
    '^': (0, -1), 'v': (0, 1), 
    '<': (-1, 0), '>': (1, 0)
}

def get_filled_grid(coords, n):
    grid = [['.'] * W for j in range(H)]
    for x, y in coords[:n]:
        grid[y][x] = '#'
    return grid

def dijkstra(grid):
    heap = [(0, 0, 0)]
    visited = {(0, 0)}
    while heap:
        d, x, y = heapq.heappop(heap)
        if x == W - 1 and y == H - 1:
            return d
        for dx, dy in DIRS.values():
            if 0 <= x+dx < W and 0 <= y+dy < H and grid[y+dy][x+dx]=='.' and (x+dx, y+dy) not in visited:
                heapq.heappush(heap, (d+1, x+dx, y+dy))
                visited.add((x+dx, y+dy))
    return False

def binary_search(coords):
    l, r = 1024, len(coords)
    while l < r - 1:
        m = (l + r) // 2
        g = get_filled_grid(coords, m)
        if dijkstra(g):
            l = m
        else:
            r = m
    return m


coords = []
input_txt = 'input.txt'
with open(input_txt) as file:
    for line in file:
        x, y = line.strip().split(',')
        coords.append((int(x), int(y)))

print("Part 1:", dijkstra(get_filled_grid(coords, 1024)))
print("Part 2:", coords[binary_search(coords)])

