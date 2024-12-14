def place_robots(robots, w, h):
    grid = [[0] * w for i in range(h)]
    for robot in robots:
        grid[robot['p'][1]][robot['p'][0]] += 1
    return grid

def print_grid(grid):
    for line in grid:
        print("".join([' ' if i == 0 else '#' for i in line]))

def move_robot(robot, grid, w, h):
    def update_position(robot):
        robot['p'][0] = (robot['p'][0] + robot['v'][0]) % w
        robot['p'][1] = (robot['p'][1] + robot['v'][1]) % h
    def update_grid(grid, robot):
        old_position = (robot['p'][0], robot['p'][1])
        update_position(robot)
        grid[old_position[1]][old_position[0]] -= 1
        grid[robot['p'][1]][robot['p'][0]] += 1
    update_grid(grid, robot)

def score_grid(grid, w, h):
    # Geometry Quadrants: I in top right, II in top left, III. bottom left, IV bottom right
    q1 = q2 = q3 = q4 = 0
    for y, line in enumerate(grid):
        for x, num in enumerate(line):
            if x < w // 2:
                if y < h // 2:
                    q2 += num
                elif y > h // 2:
                    q3 += num
            elif x > w // 2:
                if y < h // 2:
                    q1 += num
                elif y > h // 2:
                    q4 += num
    return q1 * q2 * q3 * q4

def get_longest(line):
    """Return longest run of non-zero numbers in a grid line.
    Easiest anomaly detection I can think of."""
    longest, current = 0, 0
    for num in line:
        if num > 0:
            current += 1
        else:
            longest = current if current > longest else longest
            current = 0
    return longest

input_txt = 'input.txt'

WIDTH = 101
HEIGHT = 103

robots = []
with open(input_txt) as file:
    for line in file:
        new_vel = {'p':0, 'v':0}
        p, v = line.strip().split(' ')
        p1, p2 = p.split('=')[1].split(',')
        v1, v2 = v.split('=')[1].split(',')
        robots.append({'p':[int(p1), int(p2)], 'v':[int(v1), int(v2)]})

grid = place_robots(robots, WIDTH, HEIGHT)
for s in range(100):
    for robot in robots:
        move_robot(robot, grid, WIDTH, HEIGHT)
print("Part 1", score_grid(grid, WIDTH, HEIGHT))

longest = ''
for s in range(10000):
    for robot in robots:
        move_robot(robot, grid, WIDTH, HEIGHT)
    for line in grid:
        l = get_longest(line)
        longest = '#' * l if l > len(longest) else longest
    if len(longest) > len('#######'):
        break
print_grid(grid)
print("Part 2:", s + 101)
