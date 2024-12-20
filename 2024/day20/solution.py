def get_path(lines, start, end):
    pos, visited = start, {start: None}
    while pos != end:
        x, y = pos
        for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            next_pos = (x+dx, y+dy)
            if lines[next_pos[1]][next_pos[0]] in '.SE' and next_pos not in visited:
                visited[next_pos] = pos
                pos = next_pos
                break
    path, steps = {}, 0
    while pos:
        path[pos] = steps
        steps += 1
        pos = visited[pos]
    return {s: p for p,s in {p: len(path)-1-s for p,s in path.items()}.items()} 

def taxicab(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)

def get_shortcuts(steps_coords, n, min_cut):
    shortcuts = []
    for i in range(len(steps_coords) - 1):
        curr = steps_coords[i]
        for j in range(i + min_cut, len(steps_coords)):
            if j not in steps_coords:
                continue
            comp = steps_coords[j]
            if taxicab(curr, comp) > n or j - i - taxicab(curr, comp) < min_cut:
                continue
            shortcuts.append(
                {'start': curr, 'end': comp, 'diff': j - i - taxicab(curr, comp)}
            )
    return shortcuts


input_txt = 'input.txt'
lines = []
start, end = (0, 0), (0, 0)
with open(input_txt) as file:
    for y, line in enumerate(file):
        lines.append(line.strip())
        for x, char in enumerate(line.strip()):
            if char == 'E':
                end = (x, y)
            elif char == 'S':
                start = (x, y)

path = get_path(lines, start, end)
print("Part 1:", len(get_shortcuts(path, n=2, min_cut=100)))
print("Part 2:", len(get_shortcuts(path, n=20, min_cut=100)))