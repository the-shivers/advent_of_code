input_txt = 'input.txt'
freq_dict = {}
with open(input_txt) as file:
    for y, line in enumerate(file):
        for x, chr in enumerate(line.strip()):
            if chr == '.':
                continue
            if chr in freq_dict:
                freq_dict[chr].append((x, y))
            else:
                freq_dict[chr] = [(x, y)]

height = y + 1
width = x + 1

def get_antinodes(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    dx = x2 - x1
    dy = y2 - y1
    return (x1 - dx, y1 - dy), (x2 + dx, y2 + dy)

def is_in_bounds(t1):
    x, y = t1
    return x >= 0 and x < width and y >= 0 and y < height

def get_freq_antinodes(ants):
    antinodes = set()
    for i in range(len(ants)):
        for j in range(i + 1, len(ants)):
            a1, a2 = get_antinodes(ants[i], ants[j])
            if is_in_bounds(a1):
                antinodes.add(a1)
            if is_in_bounds(a2):
                antinodes.add(a2)
    return antinodes
 
antinodes = set()
for freq, ants in freq_dict.items():
    antinodes = antinodes | get_freq_antinodes(ants)

print("Part 1:", len(antinodes))

def get_all_antinodes(t1, t2):
    antinodes = {t1, t2}
    x1, y1 = t1
    x2, y2 = t2
    dx, dy = x2 - x1, y2 - y1
    curr_x, curr_y = x1 - dx, y1 - dy
    while curr_y < height and curr_x < width and curr_y >= 0 and curr_x >= 0:
        antinodes.add((curr_x, curr_y))
        curr_x -= dx
        curr_y -= dy
    curr_x, curr_y = x2 + dx, y2 + dy
    while curr_y < height and curr_x < width and curr_y >= 0 and curr_x >= 0:
        antinodes.add((curr_x, curr_y))
        curr_x += dx
        curr_y += dy
    return antinodes

def get_all_freq_antinodes(ants):
    antinodes = set()
    for i in range(len(ants)):
        for j in range(i + 1, len(ants)):
            antinodes = antinodes | get_all_antinodes(ants[i], ants[j])
    return antinodes

antinodes = set()
for freq, ants in freq_dict.items():
    antinodes = antinodes | get_all_freq_antinodes(ants)

print("Part 2:", len(antinodes))