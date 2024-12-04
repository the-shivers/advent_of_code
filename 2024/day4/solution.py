# input_txt = 'advent_of_code/2024/day4/example.txt'
input_txt = 'advent_of_code/2024/day4/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

# Part 1
dirs = set((x, y) for x in range(-1, 2) for y in range(-1, 2)) - {(0, 0)}
count = 0
pattern = 'XMAS'
for start_y, line in enumerate(lines):
    for start_x, start_chr in enumerate(line):
        for x_dir, y_dir in dirs:
            for i, target_letter in enumerate(pattern):
                x = i * x_dir + start_x
                y = i * y_dir + start_y
                if (
                    x < 0 or x >= len(line) or # check boundaries
                    y < 0 or y >= len(lines) or 
                    lines[y][x] != target_letter
                ):
                    break
                count += 1 if i == len(pattern) - 1 else 0

print('Part 1:', count)


# Part 2
def get_a_coords(lines: list[list[str]]) -> list[tuple]:
    coords = []
    for y in range(1, len(lines) - 1): # avoid edges
        for x in range(1, len(lines[0]) - 1):
            if lines[y][x] == 'A':
                coords.append((x, y))
    return coords

def is_xmas(a_coord: tuple, lines: list[list[str]]) -> bool:
    x, y = a_coord
    tl = lines[y - 1][x - 1] # top left corner
    tr = lines[y - 1][x + 1] # top right
    bl = lines[y + 1][x - 1] # etc.
    br = lines[y + 1][x + 1]
    corners = [tl, tr, bl, br]
    return corners.count('M') == 2 and corners.count('S') == 2 and tl != br

print("Part 2:", sum(is_xmas(xy, lines) for xy in get_a_coords(lines)))