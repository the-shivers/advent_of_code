def process_line(s):
    base = [i.split(',') for i in s.strip().split(' -> ')]
    return [(int(i), int(j)) for i, j in base]

def get_lines(filename):
    with open(filename) as raw_input:
        lines = []
        for line in raw_input:
            lines.append(process_line(line))
    return lines

def interpolate(line, diag=False):
    result = []
    if line[0][0] == line[1][0]: # vert
        for i in range(min(line[0][1], line[1][1]), max(line[0][1], line[1][1]) + 1):
            result.append((line[0][0], i))
    elif line[0][1] == line[1][1]: # horiz
        for i in range(min(line[0][0], line[1][0]), max(line[0][0], line[1][0]) + 1):
            result.append((i, line[0][1]))
    elif diag: # diagonal
        start_x, start_y = line[0]
        end_x, end_y = line[1]
        for i in range(abs(start_x - end_x) + 1):
            if start_x > end_x and start_y > end_y:
                result.append((start_x - i, start_y - i))
            elif start_x > end_x and start_y < end_y:
                result.append((start_x - i, start_y + i))
            elif start_x < end_x and start_y > end_y:
                result.append((start_x + i, start_y - i))
            elif start_x < end_x and start_y < end_y:
                result.append((start_x + i, start_y + i))
    return result

def get_overlaps(lines, use_diag=False):
    coords_dict = {}
    result = 0
    for line in lines:
        for coords in interpolate(line, use_diag):
            if coords in coords_dict:
                coords_dict[coords] += 1
                if coords_dict[coords] == 2: # Avoid extra conting when 3+ lines overlap
                    result += 1
            else:
                coords_dict[coords] = 1
    return result

if __name__ == '__main__':
    filename = 'input.txt'
    lines = get_lines(filename)
    print(f'part 1 solution: {get_overlaps(lines)}') # 7436
    print(f'part 2 solution: {get_overlaps(lines, True)}') # 21104
