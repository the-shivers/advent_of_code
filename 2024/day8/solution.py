input_txt = 'input.txt'
with open(input_txt) as file:
    antennae_dict = {}
    for y, line in enumerate(file):
        for x, chr in enumerate(line.strip()):
            if chr == '.':
                continue
            if chr in antennae_dict:
                antennae_dict[chr].append((x, y))
            else:
                antennae_dict[chr] = [(x, y)]

height = y + 1
width = x + 1

def is_in_bounds(pos): return 0 <= pos[0] < width and 0 <= pos[1] < height

def get_points_in_direction(start, dx, dy):
    curr_x, curr_y = start
    while is_in_bounds((curr_x, curr_y)):
        yield (curr_x, curr_y)
        curr_x += dx
        curr_y += dy

def get_antinodes(t1, t2, get_all=False):
    (x1, y1), (x2, y2) = t1, t2
    dx, dy = x2 - x1, y2 - y1
    if not get_all:
        points = [(x1 - dx, y1 - dy), (x2 + dx, y2 + dy)]
        return {p for p in points if is_in_bounds(p)}
    backwards = get_points_in_direction((x1 - dx, y1 - dy), -dx, -dy)
    forwards = get_points_in_direction((x2 + dx, y2 + dy), dx, dy)
    return {t1, t2} | set(backwards) | set(forwards)

def get_freq_antinodes(ant_list, get_all=False):
    antinodes = set()
    for i in range(len(ant_list)):
        for j in range(i + 1, len(ant_list)):
            antinodes.update(get_antinodes(ant_list[i], ant_list[j], get_all))
    return antinodes

pt1_antinodes, pt2_antinodes = set(), set()
for freq, ants in antennae_dict.items():
    pt1_antinodes.update(get_freq_antinodes(ants, get_all=False))
    pt2_antinodes.update(get_freq_antinodes(ants, get_all=True))
print("Part 1:", len(pt1_antinodes))
print("Part 2:", len(pt2_antinodes))