input_txt = 'input.txt'
# input_txt = 'example.txt'
map = {}
instructions = []
robot = (0, 0)
with open(input_txt) as file:
    for y, line in enumerate(file):
        if len(line.strip()) == 0:
            continue
        if line.strip()[0] in '^>v<':
            instructions.append(line.strip())
        elif line.strip()[0] == '#':
            map[y] = {}
            for x, char in enumerate(line.strip()):
                map[y][x] = char
                if char == '@':
                    robot = (x, y)
    instructions = ''.join(instructions)
    
dirs = {
    'up': (0, -1),
    'right': (1, 0),
    'down': (0, 1),
    'left': (-1, 0)
}

def print_map(map):
    for rk, rv in map.items():
        row_str = ''
        for ck, cv in rv.items():
            row_str += cv
        print(row_str)

# def move_robot(robot, dir, map):
#     if move(robot, dir, map):
#         robot = (robot[0] + dir[0], robot[1] + dir[1])
#     return robot

# def move(pos, dir, map):
#     px, py = pos
#     dx, dy = dir
#     next = map[py+dy][px+dx]
#     if next == '#':
#         return False
#     elif next == '.' or move((px+dx, py+dy), dir, map):
#         map[py][px], map[py+dy][px+dx] = map[py+dy][px+dx], map[py][px]
#         return True

print_map(map)
import time

# for char in instructions:
#     if char == '^':
#         robot = move_robot(robot, dirs['up'], map)
#     elif char == '>':
#         robot = move_robot(robot, dirs['right'], map)
#     elif char == 'v':
#         robot = move_robot(robot, dirs['down'], map)
#     elif char == '<':
#         robot = move_robot(robot, dirs['left'], map)

def get_gps(map):
    gps = 0
    for rk, rv in map.items(): # rows
        for ck, cv in rv.items(): # columns
            if cv == 'O':
                gps += 100 * rk + ck
    return gps

# print(get_gps(map))

def widen_map(map):
    wide_map = {}
    for y, row in map.items():
        wide_map[y] = {}
        for x, chr in row.items():
            if chr == '#':
                wide_map[y][2 * x] = '#'
                wide_map[y][2 * x + 1] = '#'
            elif chr == 'O':
                wide_map[y][2 * x] = '['
                wide_map[y][2 * x + 1] = ']'
            elif chr == '.':
                wide_map[y][2 * x] = '.'
                wide_map[y][2 * x + 1] = '.'
            elif chr == '@':
                wide_map[y][2 * x] = '@'
                wide_map[y][2 * x + 1] = '.'
    return wide_map

wide_map = widen_map(map)
print_map(wide_map)

def l_move(pos, dir, map):
    assert dir[1] == 0 # We should only use this for lateral moves.
    px, py = pos
    dx, dy = dir
    next = map[py+dy][px+dx]
    if next == '#':
        return False
    elif next == '.' or l_move((px+dx, py+dy), dir, map):
        map[py][px], map[py+dy][px+dx] = map[py+dy][px+dx], map[py][px]
        return True
    
def v_move(pos, dir, map):
    """Moves the thing and stuff above/below it, recursively.
    If a [ or ] is told to move, moves both of them."""
    assert dir[1] != 0 # We should only use this for vertical moves.
    px, py = pos
    dx, dy = dir
    curr = map[py][px]
    next = map[py+dy][px+dx]

    def can_move(pos, dir, map):
        """Returns true if thing in position can move. Recursively checks.
        If thing is a [ or ] checks fully if the whole box can move."""
        px, py = pos
        dx, dy = dir
        curr = map[py][px]
        next = map[py+dy][px+dx]
        if curr == '@':
            if next == '#':
                return False
            elif next == '.':
                return True
            elif next in '[]':
                return can_move((px+dx, py+dy), dir, map)
        if curr == '[':
            x_mod = 1
        elif curr == ']':
            x_mod = -1
        other_next = map[py+dy][px+dx+x_mod]
        if next == '.' and other_next == '.':
            return True
        elif next in '[]' and other_next == '.':
            return can_move((px+dx,py+dy), dir, map)
        elif next == '.' and other_next in '[]':
            return can_move((px+dx+x_mod,py+dy), dir, map)
        elif next in '[]' and other_next in '[]':
            return can_move((px+dx,py+dy), dir, map) and can_move((px+dx+x_mod,py+dy), dir, map)
        elif next == '#' or other_next == '#':
            return False
        
    if next == '#':
        return False
    if curr == '@' and next == '.':
        map[py][px], map[py+dy][px+dx] = map[py+dy][px+dx], map[py][px]
        return True
    if curr == '@' and next in '[]':
        if can_move((px+dx,py+dy), dir, map):
            print('@ can move even though', next)
            v_move((px+dx,py+dy), dir, map) # Should automatically move partner
            map[py][px], map[py+dy][px+dx] = map[py+dy][px+dx], map[py][px]
            return True
        else:
            return False
    elif curr in '[]':
        print('considering', curr, 'at', px, py)
        if can_move((px,py), dir, map):
            print("Can move", curr, "!! Moving what's in front of curr", next, "at", px+dx,py+dy)
            v_move((px+dx,py+dy), dir, map)
            print("Now we moved the ",next, "at", px+dx,py+dy, "lets move curr." )
            if curr == '[':
                v_move((px+dx+1,py+dy), dir, map)
                map[py][px], map[py+dy][px+dx] = map[py+dy][px+dx], map[py][px]
                map[py][px+1], map[py+dy][px+dx+1] = map[py+dy][px+dx+1], map[py][px+1]
                return True
            else:
                v_move((px+dx-1,py+dy), dir, map)
                map[py][px], map[py+dy][px+dx] = map[py+dy][px+dx], map[py][px]
                map[py][px-1], map[py+dy][px+dx-1] = map[py+dy][px+dx-1], map[py][px-1]
                return True
        return False
    
def move_robot2(robot, char, wide_map):
    print('char', char)
    if char == '^':
        dir = dirs['up']
        print('trying vmove from', robot)
        result = v_move(robot, dirs['up'], wide_map)
    elif char == '>':
        dir = dirs['right']
        print('trying lmove from ', robot)
        result = l_move(robot, dirs['right'], wide_map)
    elif char == 'v':
        dir = dirs['down']
        print('trying vmove from', robot)
        result = v_move(robot, dirs['down'], wide_map)
    elif char == '<':
        dir = dirs['left']
        print('trying lmove from ', robot)
        result = l_move(robot, dirs['left'], wide_map)
    if result:
        robot = (robot[0] + dir[0], robot[1] + dir[1])
    return robot

robot = (robot[0] * 2, robot[1])
for i, char in enumerate(instructions):
    print(i, robot)
    robot = move_robot2(robot, char, wide_map)
    print_map(wide_map)
    # time.sleep(2)

def get_gps(map):
    gps = 0
    for rk, rv in map.items(): # rows
        for ck, cv in rv.items(): # columns
            if cv in '[O':
                gps += 100 * rk + ck
    return gps

print(get_gps(wide_map))