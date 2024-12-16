import time
start = time.time()

dirs = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0)
}

class Warehouse:
    def __init__(self, map_dict, robot_pos, is_wide=False):
        self.map = map_dict
        self.robot = robot_pos
        self.is_wide = is_wide
        
    @classmethod
    def from_file(cls, filename, is_wide=False):
        map_dict = {}
        robot = (0, 0)
        instructions = []
        with open(filename) as file:
            for y, line in enumerate(file):
                if len(line.strip()) == 0:
                    continue
                if line.strip()[0] in '^>v<':
                    instructions.append(line.strip())
                elif line.strip()[0] == '#':
                    map_dict[y] = {}
                    for x, char in enumerate(line.strip()):
                        map_dict[y][x] = char
                        if char == '@':
                            robot = (x, y)
        if not is_wide:
            return cls(map_dict, robot, is_wide), ''.join(instructions)
        wide_map = {}
        for y, row in map_dict.items():
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
        return cls(wide_map, (robot[0]*2, robot[1]), is_wide), ''.join(instructions)
        
    def h_move(self, pos, dir):
        """Part 1 movement or part 2 horizontal movement."""
        px, py = pos
        dx, dy = dir
        next = self.map[py+dy][px+dx]
        if next == '#':
            return False
        elif next == '.' or self.h_move((px+dx, py+dy), dir):
            self.map[py][px], self.map[py+dy][px+dx] = self.map[py+dy][px+dx], self.map[py][px]
            return True
        
    def can_v_move(self, pos, dir):
        """Pt2 Only. Vertical moves only. Returns true if thing in position can move. 
        Recursively checks. If thing is a [ or ] checks fully if the whole box can move."""
        px, py = pos
        dx, dy = dir
        curr = self.map[py][px]
        next = self.map[py+dy][px+dx]
        # If we're moving the lil robot...
        if curr == '@':
            if next == '#':
                return False
            elif next == '.':
                return True
            elif next in '[]':
                return self.can_v_move((px+dx, py+dy), dir) # Will check both box parts
        # If we're moving a wide box
        x_mod = 1 if curr == '[' else -1
        other_next = self.map[py+dy][px+dx+x_mod]
        if next == '.' and other_next == '.':
            return True
        elif next in '[]' and other_next == '.':
            return self.can_v_move((px+dx,py+dy), dir)
        elif next == '.' and other_next in '[]':
            return self.can_v_move((px+dx+x_mod,py+dy), dir)
        elif next in '[]' and other_next in '[]':
            return (
                self.can_v_move((px+dx,py+dy), dir) and 
                self.can_v_move((px+dx+x_mod,py+dy), dir)
            )
        return False
        
    def v_move(self, pos, dir):
        """Moves the thing and stuff above/below it, recursively.
        If a [ or ] is told to move, moves both of them."""
        px, py = pos
        dx, dy = dir
        curr = self.map[py][px]
        next = self.map[py+dy][px+dx]
        if self.can_v_move(pos, dir):
            if next in '[]':
                self.v_move((px+dx, py+dy), dir)
            self.map[py][px], self.map[py+dy][px+dx] = self.map[py+dy][px+dx], self.map[py][px]
            if curr in '[]':
                x_mod = 1 if curr == '[' else -1
                if self.map[py+dy][px+dx+x_mod] in '[]':
                    self.v_move((px+dx+x_mod, py+dy), dir)
                self.map[py][px+x_mod], self.map[py+dy][px+dx+x_mod] = self.map[py+dy][px+dx+x_mod], self.map[py][px+x_mod]
            return True
        return False
        
    def move_robot(self, dir):
        if self.is_wide and dir[1] != 0:  # pt2 and vertical
            success = self.v_move(self.robot, dir)
        else:                             # pt1 or pt2 horizontal
            success = self.h_move(self.robot, dir)
        if success:
            self.robot = (self.robot[0] + dir[0], self.robot[1] + dir[1])
        
    def get_gps(self):
        gps = 0
        for rk, rv in self.map.items():
            for ck, cv in rv.items():
                if cv in '[O':
                    gps += 100 * rk + ck
        return gps
    
    def print(self):
        for rv in self.map.values():
            row_str = ''
            for cv in rv.values():
                row_str += cv
            print(row_str)


def solve(filename, part=1):
    warehouse, instructions = Warehouse.from_file(filename, is_wide=(part==2))
    for char in instructions:
        warehouse.move_robot(dirs[char])
    return warehouse.get_gps()

print("Part 1:", solve('input.txt', 1))
print("Part 2:", solve('input.txt', 2))
elapsed = time.time() - start

# Format differently based on the duration
if elapsed < 0.001:
    print(f"Execution time: {elapsed*1000000:.2f} microseconds")
elif elapsed < 1:
    print(f"Execution time: {elapsed*1000:.2f} milliseconds")
else:
    print(f"Execution time: {elapsed:.4f} seconds")