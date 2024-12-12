def get_3x3(x, y, lines):
    height = len(lines)
    width = len(lines[0])
    grid = []
    # Build 3x3 grid with '$' for out of bounds
    for dy in [-1, 0, 1]:
        row = []
        for dx in [-1, 0, 1]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                row.append(lines[ny][nx])
            else:
                row.append('$')
        grid.append(row)
    return grid

def count_cell_corners(x, y, lines):
    corners = 0
    grid = get_3x3(x, y, lines)
    print(grid)
    curr = grid[1][1]  # Center cell
    # Exterior corners (when missing two adjacent neighbors)
    # Top left
    if grid[0][1] != curr and grid[1][0] != curr:
        corners += 1
    # Top right    
    if grid[0][1] != curr and grid[1][2] != curr:
        corners += 1
    # Bottom left    
    if grid[2][1] != curr and grid[1][0] != curr:
        corners += 1
    # Bottom right    
    if grid[2][1] != curr and grid[1][2] != curr:
        corners += 1
    print('returning corners', corners)
    return corners

def get_region(curr, area, bounds, corners, lines):
    x, y = curr
    corners += count_cell_corners(x, y, lines)  # Count corners for initial cell
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if (new_x, new_y) in area or ((new_x, new_y), (dx, dy)) in bounds:
            continue
        if 0 <= new_x < width and 0 <= new_y < height:
            if lines[new_y][new_x] == lines[y][x]:
                area.add((new_x, new_y))
                # Just add the corners for this new cell
                corners += count_cell_corners(new_x, new_y, lines)
                # Continue exploring from this cell
                get_region((new_x, new_y), area, bounds, corners, lines)
            else:
                bounds.add(((new_x, new_y), (dx, dy)))
        else:
            bounds.add(((new_x, new_y), (dx, dy)))
    
    return area, bounds, corners


input_txt = 'example6.txt'
with open(input_txt) as file:
    lines = [list(line.strip()) for line in file]

height = len(lines)
width = len(lines[0])

pt1 = pt2 = 0
area_coords = {}
for y, line in enumerate(lines):
    for x, chr in enumerate(line):
        if (x, y) not in area_coords:
            a, b, corners = get_region((x, y), {(x, y)}, set(), 0, [l[:] for l in lines])
            pt1_sides = len(b)
            pt2_sides = corners
            print('area', len(a))
            print('pt2 sides', corners)
            area_coords.update({(x, y): chr for (x, y) in a})
            pt1 += len(a) * pt1_sides
            pt2 += len(a) * pt2_sides

print("Part 1:", pt1) # 1434856
print("Part 2:", pt2) # 891106
