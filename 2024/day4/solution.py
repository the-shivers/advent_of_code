# input_txt = 'advent_of_code/2024/day4/example.txt'
input_txt = 'advent_of_code/2024/day4/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

# Part 1
pat = 'XMAS'

def find_horizontal_matches(lines, pattern):
    counter = 0
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0]) - 3):
            for p in [pattern, pattern[::-1]]:
                if (
                    lines[y][x] == p[0] and 
                    lines[y][x + 1] == p[1] and
                    lines[y][x + 2] == p[2] and
                    lines[y][x + 3] == p[3]
                ):
                    counter += 1
    return counter

def find_vertical_matches(lines, pattern):
    counter = 0
    for y in range(0, len(lines) - 3):
        for x in range(0, len(lines[0])):
            for p in [pattern, pattern[::-1]]:
                if (
                    lines[y][x] == p[0] and 
                    lines[y + 1][x] == p[1] and
                    lines[y + 2][x] == p[2] and
                    lines[y + 3][x] == p[3]
                ):
                    counter += 1
    return counter

def find_diagonal_uphill_matches(lines, pattern):
    counter = 0
    for y in range(3, len(lines)):
        for x in range(0, len(lines[0]) - 3):
            for p in [pattern, pattern[::-1]]:
                if (
                    lines[y][x] == p[0] and 
                    lines[y - 1][x + 1] == p[1] and
                    lines[y - 2][x + 2] == p[2] and
                    lines[y - 3][x + 3] == p[3]
                ):
                    counter += 1
    return counter


def find_diagonal_downhill_matches(lines, pattern):
    counter = 0
    for y in range(0, len(lines) - 3):
        for x in range(0, len(lines[0]) - 3):
            for p in [pattern, pattern[::-1]]:
                if (
                    lines[y][x] == p[0] and 
                    lines[y + 1][x + 1] == p[1] and
                    lines[y + 2][x + 2] == p[2] and
                    lines[y + 3][x + 3] == p[3]
                ):
                    counter += 1
    return counter

print("Part 1:",
    find_horizontal_matches(lines, pattern=pat) + \
    find_vertical_matches(lines, pattern=pat) + \
    find_diagonal_uphill_matches(lines, pattern=pat) + \
    find_diagonal_downhill_matches(lines, pattern=pat)
)

# Part 2
def get_a_coords(lines):
    coords = []
    for y, line in enumerate(lines):
        if y == 0 or y == len(lines) - 1:
            continue
        for x, chr in enumerate(line):
            if x == 0 or x == len(line) - 1:
                continue
            if chr == 'A':
                coords.append((x, y))
    return coords

def is_xmas(xy: tuple, lines: list[list[str]]) -> bool:
    x, y = xy
    top_left = lines[y - 1][x - 1]
    top_right = lines[y - 1][x + 1]
    bottom_left = lines[y + 1][x - 1]
    bottom_right = lines[y + 1][x + 1]
    corners = [top_left, top_right, bottom_left, bottom_right]
    if corners.count('M') == 2 and corners.count('S') == 2 and top_left != bottom_right:
        return True
    return False

count = 0
for coords in get_a_coords(lines):
    if is_xmas(coords, lines):
        count += 1
print("Part 2:", count)
