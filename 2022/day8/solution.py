example = 'advent_of_code/2022/day8/example.txt'
input_txt = 'advent_of_code/2022/day8/input.txt'
with open(input_txt) as file:
    grid = [line.strip() for line in file]

def get_west_visibility(x, y, grid): # Can you see it FROM the west
    if max(grid[y][0:x]) >= grid[y][x]:
        return False
    else:
        return True
        
def get_east_visibility(x, y, grid): # Can you see it FROM the east
    if max(grid[y][x + 1:]) >= grid[y][x]:
        return False
    else:
        return True
    
def get_north_visibility(x, y, grid): # Can you see it FROM the north
    if max(row[x] for row in grid[0:y]) >= grid[y][x]:
        return False
    else:
        return True
    
def get_south_visibility(x, y, grid): # Can you see it FROM the south
    if max(row[x] for row in grid[y + 1:]) >= grid[y][x]:
        return False
    else:
        return True
    
def get_visibility(x, y, grid):
    if x == 0 or y == 0 or x == len(grid[y]) - 1 or y == len(grid) - 1:
        return True
    west = get_west_visibility(x, y, grid)
    east = get_east_visibility(x, y, grid)
    north = get_north_visibility(x, y, grid)
    south = get_south_visibility(x, y, grid)
    if west or east or north or south:
        return True
    else:
        return False
    
visible_trees = 0
vis_grid = []
for y, row in enumerate(grid):
    vis_grid.append([])
    for x in range(len(row)):
        if get_visibility(x, y, grid):
            visible_trees += 1
            vis_grid[y].append(1)
        else:
            vis_grid[y].append(0)
            
print('Part 1:', visible_trees) # 1870

# Part 2
def count_viewable_trees(tree_height, view_string):
    counter = 0
    for tree in view_string:
        counter += 1
        if tree_height <= tree:
            break
    return counter

def calculate_scenic_score(x, y, grid):
    west_view = grid[y][0:x][::-1]
    east_view = grid[y][x+1:]
    north_view = ''.join([grid[i][x] for i in range(y)][::-1])
    south_view = ''.join([grid[i][x] for i in range(y+1, len(grid))])
    scenic_score_e = count_viewable_trees(grid[y][x], west_view)
    scenic_score_w = count_viewable_trees(grid[y][x], east_view)
    scenic_score_n = count_viewable_trees(grid[y][x], north_view)
    scenic_score_s = count_viewable_trees(grid[y][x], south_view)
    return scenic_score_e * scenic_score_w * scenic_score_n * scenic_score_s

max_score = 0
for y, row in enumerate(grid):
    for x in range(len(row)):
        score = calculate_scenic_score(x, y, grid)
        if score > max_score:
            max_score = score
             
print('Part 2:', max_score) # 517440
