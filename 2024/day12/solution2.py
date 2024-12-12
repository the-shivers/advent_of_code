def get_region_info(pos, grid):
    """
    Gets region information starting from a position, returns (region, perimeter, corners).
    Uses pattern matching on 3x3 grids to detect corners.
    """
    def get_3x3(pos):
        y, x = pos
        return [[grid[y+dy][x+dx] if 0 <= y+dy < len(grid) and 0 <= x+dx < len(grid[0])
                else '$' for dx in [-1,0,1]] for dy in [-1,0,1]]
    
    def count_corners(pos):
        grid_3x3 = get_3x3(pos)
        center = grid_3x3[1][1]
        
        # Define corner patterns more concisely
        corner_patterns = [
            # External corners (adjacent cells different)
            ((0,1), (1,0)),  # Top-left
            ((0,1), (1,2)),  # Top-right
            ((2,1), (1,0)),  # Bottom-left
            ((2,1), (1,2)),  # Bottom-right
            
            # Internal corners (adjacent cells same, diagonal different)
            ((0,1,1,2,0,2), True),   # Top-right
            ((0,1,1,0,0,0), True),   # Top-left
            ((2,1,1,2,2,2), True),   # Bottom-right
            ((2,1,1,0,2,0), True)    # Bottom-left
        ]
        
        corners = 0
        # Check external corners
        for (y1,x1), (y2,x2) in corner_patterns[:4]:
            if grid_3x3[y1][x1] != center and grid_3x3[y2][x2] != center:
                corners += 1
        
        # Check internal corners
        for (y1,x1,y2,x2,y3,x3), _ in corner_patterns[4:]:
            if (grid_3x3[y1][x1] == center and 
                grid_3x3[y2][x2] == center and 
                grid_3x3[y3][x3] != center):
                corners += 1
                
        return corners
    
    def flood_fill(curr_pos, region):
        if curr_pos in region:
            return
        
        y, x = curr_pos
        if not (0 <= y < len(grid) and 0 <= x < len(grid[0])):
            return
            
        if grid[y][x] != grid[pos[0]][pos[1]]:
            return
            
        region.add(curr_pos)
        for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
            flood_fill((y+dy, x+dx), region)
    
    region = set()
    flood_fill(pos, region)
    
    corners = sum(count_corners((y,x)) for y,x in region)
    perimeter = sum(1 for y,x in region
                   for dy,dx in [(0,1), (1,0), (0,-1), (-1,0)]
                   if not (0 <= y+dy < len(grid) and 0 <= x+dx < len(grid[0]))
                   or grid[y+dy][x+dx] != grid[y][x])
    
    return region, perimeter, corners

def solve_garden_groups(filename):
    """Solves both parts of the garden groups puzzle."""
    with open(filename) as f:
        grid = [list(line.strip()) for line in f]
    
    visited = set()
    price_p1 = price_p2 = 0
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (y,x) not in visited:
                region, perimeter, corners = get_region_info((y,x), grid)
                visited.update(region)
                price_p1 += len(region) * perimeter
                price_p2 += len(region) * corners
    
    return price_p1, price_p2

if __name__ == "__main__":
    part1, part2 = solve_garden_groups('input.txt')
    print(f"Part 1: {part1}")  # 1434856
    print(f"Part 2: {part2}")  # 891106
    