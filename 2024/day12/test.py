def count_corners(grid):
    # Pad the grid with '$' on all sides to avoid boundary checking
    padded = [['$'] * (len(grid[0]) + 2)]
    for row in grid:
        padded.append(['$'] + row + ['$'])
    padded.append(['$'] * (len(grid[0]) + 2))
    corners = 0
    seen = set()
    def count(y, x):
        if (y,x) in seen or padded[y][x] == '$':
            return
        seen.add((y,x))
        nonlocal corners
        curr = padded[y][x]
        # Exterior corners - when missing two adjacent neighbors
        # Top left
        if padded[y-1][x] != curr and padded[y][x-1] != curr:
            print('exteriora', x, y)
            corners += 1
        # Top right
        if padded[y-1][x] != curr and padded[y][x+1] != curr:
            corners += 1
            print('exteriorb', x, y)
        # Bottom left    
        if padded[y+1][x] != curr and padded[y][x-1] != curr:
            corners += 1
            print('exteriorc', x, y)
        # Bottom right
        if padded[y+1][x] != curr and padded[y][x+1] != curr:
            corners += 1
            print('exteriord', x, y)
        # Interior corners - two types:
        # 1. Has two adjacent cells but missing diagonal
        # Top right quadrant
        if padded[y-1][x] == curr and padded[y][x+1] == curr and padded[y-1][x+1] != curr:
            corners += 1
            print('interior1a', x, y)
        # Top left quadrant    
        if padded[y-1][x] == curr and padded[y][x-1] == curr and padded[y-1][x-1] != curr:
            corners += 1
            print('interior1b', x, y)
        # Bottom right quadrant    
        if padded[y+1][x] == curr and padded[y][x+1] == curr and padded[y+1][x+1] != curr:
            corners += 1
            print('interior1c', x, y)
        # Bottom left quadrant    
        if padded[y+1][x] == curr and padded[y][x-1] == curr and padded[y+1][x-1] != curr:
            corners += 1
            print('interior1d', x, y)
        
        # Only recurse to matching neighbors
        if padded[y-1][x] == curr:
            count(y-1, x)
        if padded[y+1][x] == curr:
            count(y+1, x)
        if padded[y][x-1] == curr:
            count(y, x-1)
        if padded[y][x+1] == curr:
            count(y, x+1)
    
    regions_total = 0
    for y in range(1, len(padded)-1):
        for x in range(1, len(padded[0])-1):
            if padded[y][x] not in  ('$', '.') and (y,x) not in seen:
                corners = 0
                region_char = padded[y][x]
                count(y, x)
                print('corners', corners)
                region_size = sum(1 for (py,px) in seen if padded[py][px] == region_char)
                print('size', region_size)
                regions_total += region_size * corners
    
    return regions_total

input_txt = 'example7.txt'
with open(input_txt) as file:
    lines = [list(line.strip()) for line in file]

print(count_corners(lines))