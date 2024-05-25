pipes = {
    '|': ('north', 'south'),
    '-': ('east', 'west'),
    'L': ('north', 'east'),
    'J': ('north', 'west'),
    '7': ('south', 'west'),
    'F': ('south', 'east')
}


def get_puzzle(filepath: str) -> list:
    with open(filepath) as lines:
        return [line.strip() for line in lines]


# Part 1

def get_direction(current_loc: tuple, prev_loc: tuple) -> str:
    """
    Given your previous location and current location, returns a 
    string representing the compass direction of your previous location.
    
    e.g. assume (0, 0) in top left corner and (n, n) in bottom right corner.
    given current_location = (0, 0) for our (x, y) coordinates, and
    given prev_loc = (1, 0) for our previous (x, y) coordinates, this
    function will return "east" since our previous location was east of us.
    """
    x_change = current_loc[0] - prev_loc[0]
    y_change = current_loc[1] - prev_loc[1]
    if (x_change != 0 and y_change !=0) or (x_change == 0 and y_change == 0):
        raise Exception(f'Invalid movement! {prev_loc} to {current_loc}')
    elif x_change == 0:
        return 'north' if y_change > 0 else 'south'
    else:
        return 'west' if x_change > 0 else 'east'
    
def get_start_direction(start_loc: tuple, puzzle: list) -> str:
    # check north (directions that touch south)
    if start_loc[1] > 0 and puzzle[start_loc[1] - 1][start_loc[0]] in ('|', '7', 'F'):
        return 'north'
    # check east (directions that touch west)
    if start_loc[0] < len(puzzle[0]) - 1 and puzzle[start_loc[1]][start_loc[0] + 1] in ('-', 'J', '7'):
        return 'east'
    # check south (directions that touch north)
    if start_loc[1] < len(puzzle) - 1 and puzzle[start_loc[1] + 1][start_loc[0]] in ('|', 'L', 'J'):
        return 'south'
    # check west (directions that touch east)
    if start_loc[0] > 0 and puzzle[start_loc[1]][start_loc[0] - 1] in ('-', 'L', 'F'):
        return 'west'

def navigate_step(current_loc: tuple, prev_loc: tuple, puzzle: list, pipes: dict) -> tuple:
    # Identify next direction to move in
    current_symbol = puzzle[current_loc[1]][current_loc[0]]
    if current_symbol == 'S':
        next_direction = get_start_direction(current_loc, puzzle)
    elif current_symbol == '.':
        raise Exception("You shouldn't be there! That's not a pipe! (.)")
    elif current_symbol in pipes:
        previous_direction = get_direction(current_loc, prev_loc)
        next_direction = (set(pipes[current_symbol]) - {previous_direction}).pop()
    else:
        raise Exception(f'Invalid symbol! {current_symbol}')
    # Movement
    if next_direction == 'north':
        if current_loc[1] == 0:
            raise Exception(f"Can't head north! (Current Location: {current_loc})")
        return (current_loc[0], current_loc[1] - 1)
    elif next_direction == 'east':
        if current_loc[0] == len(puzzle[0]) - 1:
            raise Exception(f"Can't head east! (Current Location: {current_loc})")
        return (current_loc[0] + 1, current_loc[1])
    elif next_direction == 'south':
        if current_loc[1] == len(puzzle) - 1:
            raise Exception(f"Can't head south! (Current Location: {current_loc})")
        return (current_loc[0], current_loc[1] + 1)
    elif next_direction == 'west':
        if current_loc[0] == 0:
            raise Exception(f"Can't head west! (Current Location: {current_loc})")
        return (current_loc[0] - 1, current_loc[1])
    else:
        raise Exception(f'next_direction = {next_direction} not a valid direction!')
    
def find_start(puzzle: list) -> tuple:
    for y, row in enumerate(puzzle):
        for x, symbol in enumerate(row):
            if symbol == 'S':
                return (x, y)
            
def solve_part_1(filepath: str, max_steps: int = 100000) -> int:
    puzzle = get_puzzle(filepath)
    current_location = find_start(puzzle)
    previous_location = ()
    previous_location, current_location = current_location, navigate_step(current_location, previous_location, puzzle, pipes)
    counter = 1
    while puzzle[current_location[1]][current_location[0]] != 'S':
        previous_location, current_location = current_location, navigate_step(current_location, previous_location, puzzle, pipes)
        counter += 1
        if counter >= max_steps:
            break
    return int(float(counter) / 2)


# Part 2

def solve_part_1_with_extras(filepath: str, max_steps: int = 100000) -> int:
    """Returns a list representing the symbol and coordinates of each item in the path."""
    puzzle = get_puzzle(filepath)
    new_puzzle = [list(i) for i in puzzle]
    current_location = find_start(new_puzzle)
    previous_location = ()
    previous_location, current_location = current_location, navigate_step(current_location, previous_location, new_puzzle, pipes)
    counter = 1
    path_list = [('S', previous_location), (new_puzzle[current_location[1]][current_location[0]], current_location)]
    while new_puzzle[current_location[1]][current_location[0]] != 'S':
        previous_location, current_location = current_location, navigate_step(current_location, previous_location, new_puzzle, pipes)
        path_list.append((new_puzzle[current_location[1]][current_location[0]], current_location))
        counter += 1
        if counter >= max_steps:
            break
    return int(float(counter) / 2), path_list

def get_clean_puzzle(puzzle, path_list):
    """Kind of a stupid function that rebuilds the puzzle, substituting all non-path coordinates with an empty space."""
    # build clean puzzle like an idiot
    clean_puzzle = []
    for y, row in enumerate(puzzle):
        clean_row = []
        for x, symb in enumerate(row):
            clean_row.append(' ')
        clean_puzzle.append(clean_row)
    # populate old path
    for symbol, (x, y) in path_list:
        clean_puzzle[y][x] = symbol
    return [''.join(i) for i in clean_puzzle]

def is_inside(clean_puzzle, coords):
    """
    Explore to the right of a coordinate in the clean puzzle. If we hit an odd number of vertical lines, we're inside.
    U bends are ignored, zig-zaggies are counted.
    Learned this doing some geometry work a million years ago. Makes sense if you think about it.

    | = a vertical line.
    - = ignored.
    space = ignored.
    L7, L-7, L--7, etc. = a vertical line
    FJ, F-J, F--J, etc. = a vertical line
    LJ, L-J, L--J, etc. = ignored
    F7, F-7, F--7, etc. = ignored

    """
    to_right = clean_puzzle[coords[1]][coords[0]+1:]
    to_right = to_right.replace(' ', '').replace('-', '').replace('LJ', '').replace('F7', '').replace('L7', '|').replace('FJ', '|')
    return len(to_right) % 2 == 1 # if odd, inside

def solve_part_2(filepath):
    puzzle = get_puzzle(filepath)
    solution, path_list = solve_part_1_with_extras(filepath)
    clean_puzzle = get_clean_puzzle(puzzle, path_list)
    counter = 0
    for y in range(len(clean_puzzle)):
        for x in range(len(clean_puzzle[0])):
            if clean_puzzle[y][x] == ' ' and is_inside(clean_puzzle, (x, y)):
                counter += 1
    return counter

# Results
filename = 'input.txt'
print(solve_part_1(filename)) # 6768
print(solve_part_2(filename)) # 351

# Demo of clean puzzle printing, just for kicks.
filename = 'example3.txt'
puzzle = get_puzzle(filename)
solution, path_list = solve_part_1_with_extras(filename)
clean_puzzle = get_clean_puzzle(puzzle, path_list)
print('\n'.join(clean_puzzle))