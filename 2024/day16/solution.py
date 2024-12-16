from collections import deque

dirs = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0)
}

def get_start_pos(grid):
    for y, line in enumerate(grid):
        for x, chr in enumerate(line):
            if chr == 'S':
                return (x, y)

def explore_iterative(start_pos, start_dir, grid):
    queue = deque([(start_pos, start_dir, 0)])
    steps_so_far = {(start_pos[0], start_pos[1], start_dir): 0}
    while queue:
        pos, dir, curr_score = queue.popleft()
        px, py = pos
        dx, dy = dirs[dir]
        # Base case (done)
        if grid[py][px] == 'E':
            continue
        # Forward
        if grid[py+dy][px+dx] in 'E.':
            new_score = curr_score + 1
            new_key = (px+dx, py+dy, dir)
            if new_key not in steps_so_far or new_score < steps_so_far[new_key]:
                steps_so_far[new_key] = new_score
                queue.append(((px+dx, py+dy), dir, new_score))
        # Turns
        turns = []
        if dir == '^':
            if grid[py][px-1] == '.': turns.append('<')
            if grid[py][px+1] == '.': turns.append('>')
        elif dir == '>':
            if grid[py-1][px] == '.': turns.append('^')
            if grid[py+1][px] == '.': turns.append('v')
        elif dir == 'v':
            if grid[py][px+1] == '.': turns.append('>')
            if grid[py][px-1] == '.': turns.append('<')
        elif dir == '<':
            if grid[py+1][px] == '.': turns.append('v')
            if grid[py-1][px] == '.': turns.append('^')
        for new_dir in turns:
            new_score = curr_score + 1000
            new_key = (px, py, new_dir)
            if new_key not in steps_so_far or new_score < steps_so_far[new_key]:
                steps_so_far[new_key] = new_score
                queue.append((pos, new_dir, new_score))
    min_score = float('inf')
    for (x, y, d), score in steps_so_far.items():
        if grid[y][x] == 'E':
            min_score = min(min_score, score)
    return min_score if min_score != float('inf') else None

input_txt = 'input.txt'
with open(input_txt) as file:
    grid = [list(line.strip()) for line in file]

start_pos = get_start_pos(grid)
result = explore_iterative(start_pos, '>', grid)
print("Part 1:", result)



#  Part 2
from collections import deque, defaultdict

def explore_with_deque(start_pos, start_dir, grid, target_score=103512):
    # Regular queue instead of priority queue
    queue = deque([(start_pos, start_dir, 0)])
    steps_so_far = defaultdict(dict)
    steps_so_far[(start_pos[0], start_pos[1], start_dir)] = {
        'min_score': 0,
        'visited': {start_pos}
    }
    
    while queue:
        pos, dir, curr_score = queue.popleft()  # popleft instead of heappop
        if curr_score > target_score:
            continue
        px, py = pos
        dx, dy = dirs[dir]
        if grid[py][px] == 'E' and curr_score == target_score:
            continue
        # Forward movement
        if grid[py+dy][px+dx] in 'E.':
            new_score = curr_score + 1
            if new_score <= target_score:
                new_key = (px+dx, py+dy, dir)
                new_visited = steps_so_far[(px, py, dir)]['visited'].copy()
                new_visited.add((px+dx, py+dy))
                
                if (new_key not in steps_so_far or 
                    new_score <= steps_so_far[new_key]['min_score']):
                    if new_key not in steps_so_far or new_score < steps_so_far[new_key]['min_score']:
                        steps_so_far[new_key] = {
                            'min_score': new_score,
                            'visited': new_visited
                        }
                        queue.append(((px+dx, py+dy), dir, new_score))  # append instead of heappush
                    else:  # equal scores
                        steps_so_far[new_key]['visited'].update(new_visited)
        
        # Handle turns (only if resulting score wouldn't exceed target)
        if curr_score + 1000 <= target_score:
            turns = []
            if dir == '^':
                if grid[py][px-1] == '.': turns.append('<')
                if grid[py][px+1] == '.': turns.append('>')
            elif dir == '>':
                if grid[py-1][px] == '.': turns.append('^')
                if grid[py+1][px] == '.': turns.append('v')
            elif dir == 'v':
                if grid[py][px+1] == '.': turns.append('>')
                if grid[py][px-1] == '.': turns.append('<')
            elif dir == '<':
                if grid[py+1][px] == '.': turns.append('v')
                if grid[py-1][px] == '.': turns.append('^')
                
            for new_dir in turns:
                new_score = curr_score + 1000
                new_key = (px, py, new_dir)
                new_visited = steps_so_far[(px, py, dir)]['visited'].copy()
                
                if (new_key not in steps_so_far or 
                    new_score <= steps_so_far[new_key]['min_score']):
                    if new_key not in steps_so_far or new_score < steps_so_far[new_key]['min_score']:
                        steps_so_far[new_key] = {
                            'min_score': new_score,
                            'visited': new_visited
                        }
                        queue.append((pos, new_dir, new_score))  # append instead of heappush
                    else:  # equal scores
                        steps_so_far[new_key]['visited'].update(new_visited)
    
    # Collect all visited tiles from optimal paths
    final_visited = set()
    for (x, y, d), vals in steps_so_far.items():
        if grid[y][x] == 'E' and vals['min_score'] == target_score:
            final_visited.update(vals['visited'])
    
    return final_visited

# Reading input
input_txt = 'input.txt'
with open(input_txt) as file:
    grid = [list(line.strip()) for line in file]

start_pos = get_start_pos(grid)
result = explore_with_deque(start_pos, '>', grid, target_score=103512)
print("Part 2:", len(result))