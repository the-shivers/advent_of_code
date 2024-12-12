def get_region(curr, area, bounds, lines):
    """Recursively explore continuous area."""
    x, y = curr
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if (new_x, new_y) in area or ((new_x, new_y), (dx, dy)) in bounds:
            continue
        if 0 <= new_x < len(lines[0]) and 0 <= new_y < len(lines):
            if lines[new_y][new_x] == lines[y][x]:
                area.add((new_x, new_y))
                get_region((new_x, new_y), area, bounds, lines)
            else:
                bounds.add(((new_x, new_y), (dx, dy)))
        else:
            bounds.add(((new_x, new_y), (dx, dy)))
    return area, bounds

def get_leftmost_upper_bound(bounds_set):
    """Find the leftmost point of the uppermost boundary."""
    min_y = float('inf')
    for (x, y), (dx, dy) in bounds_set:
        if (dx, dy) == (0, -1):  # Top boundary
            min_y = min(min_y, y)
            
    best_bound = ((float('inf'), float('inf')), (0, -1))
    for bound in bounds_set:
        (x, y), (dx, dy) = bound
        if (dx, dy) == (0, -1) and y == min_y:
            if x < best_bound[0][0]:
                best_bound = bound
    return best_bound

def get_continuous_sides(bounds_set):
    """Count continuous sides by following the boundary path."""
    if not bounds_set:
        return 0
        
    curr = get_leftmost_upper_bound(bounds_set)
    bounds_set.remove(curr)
    sides = 1
    
    while bounds_set:
        (curr_x, curr_y), (dx, dy) = curr
        found_next = False
        
        # Direction-specific transitions
        if (dx, dy) == (0, 1):  # Moving down
            possible_moves = [
                ((curr_x - 1, curr_y), (0, 1)),     # Continue down
                ((curr_x - 1, curr_y - 1), (-1, 0)), # Turn left
                ((curr_x, curr_y), (1, 0))          # Turn right
            ]
        elif (dx, dy) == (-1, 0):  # Moving left
            possible_moves = [
                ((curr_x, curr_y - 1), (-1, 0)),    # Continue left
                ((curr_x + 1, curr_y - 1), (0, -1)), # Turn up
                ((curr_x, curr_y), (0, 1))          # Turn down
            ]
        elif (dx, dy) == (0, -1):  # Moving up
            possible_moves = [
                ((curr_x + 1, curr_y), (0, -1)),    # Continue up
                ((curr_x + 1, curr_y + 1), (1, 0)), # Turn right
                ((curr_x, curr_y), (-1, 0))         # Turn left
            ]
        elif (dx, dy) == (1, 0):  # Moving right
            possible_moves = [
                ((curr_x, curr_y + 1), (1, 0)),     # Continue right
                ((curr_x - 1, curr_y + 1), (0, 1)), # Turn down
                ((curr_x, curr_y), (0, -1))         # Turn up
            ]
            
        # Try each possible move in priority order
        for next_move in possible_moves:
            if next_move in bounds_set:
                if next_move[1] != curr[1]:  # Direction changed
                    sides += 1
                bounds_set.remove(next_move)
                curr = next_move
                found_next = True
                break
                
        if not found_next:
            # Start new trace from remaining boundaries
            curr = get_leftmost_upper_bound(bounds_set)
            bounds_set.remove(curr)
            sides += 1
            
    return sides

def solve(lines):
    area_coords = {}
    pt1 = pt2 = 0
    
    for y, line in enumerate(lines):
        for x, chr in enumerate(line):
            if (x, y) not in area_coords:
                area, bounds = get_region((x, y), {(x, y)}, set(), [l[:] for l in lines])
                pt1_sides = len(bounds)
                pt2_sides = get_continuous_sides(bounds)
                area_coords.update({(x, y): chr for (x, y) in area})
                pt1 += len(area) * pt1_sides
                pt2 += len(area) * pt2_sides
                
    return pt1, pt2

if __name__ == "__main__":
    with open('input.txt') as file:
        lines = [list(line.strip()) for line in file]
        
    pt1, pt2 = solve(lines)
    print(f"Part 1: {pt1}")  # 1434856
    print(f"Part 2: {pt2}")  # 891106