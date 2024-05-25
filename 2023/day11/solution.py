

def get_puzzle(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]

def expand_rows(puzzle):
    new_puzzle = [] # To avoid modifying the original puzzle
    for row in puzzle:
        new_puzzle.append(str(row)) # Always add this
        if row.find('#') == -1:
            new_puzzle.append(str(row))
    return new_puzzle

def expand_cols(puzzle):
    # Loop through once to identify columns to expand
    expand_list = [True for i in puzzle[0]]
    for row in puzzle:
        for i, character in enumerate(row):
            if character == '#':
                expand_list[i] = False
    # Loop through again to expand, a la expand_rows
    new_puzzle = []
    for row in puzzle:
        new_row = []
        for i, (symbol, boolean) in enumerate(zip(row, expand_list)):
            new_row.append(symbol) # Always add this
            if boolean:
                new_row.append('.')
        new_puzzle.append(''.join(new_row))
    return new_puzzle

def get_galaxy_coords(expanded_puzzle):
    galaxies = []
    for y, row in enumerate(expanded_puzzle):
        for x, symbol in enumerate(row):
            if symbol == '.':
                continue
            galaxies.append((x, y))
    return galaxies

def get_distance(coords1, coords2):
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])

def sum_distances(galaxies):
    total = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            total += get_distance(galaxies[i], galaxies[j])
    return total

def part_1(filename):
    puzzle = get_puzzle(filename)
    expanded_rows = expand_rows(puzzle)
    expanded = expand_cols(expanded_rows)
    galaxies = get_galaxy_coords(expanded)
    return sum_distances(galaxies)


# Part 2

# Blast! Thwarted again! Instead of trying to brute force, we can compute intelligently.
# We won't make a 10 million by 10 million grid. Instead, we will just know that when we cross
# Gaps, we need to add one million to our distance estimate. Kinda bullshit that it doesn't
# actually tell us the answer for the example lol.

def get_row_gaps(puzzle):
    """Return a list of bools showing True where expansions occur."""
    row_gaps = []
    for row in puzzle:
        if row.find('#') == -1:
            row_gaps.append(True)
        else:
            row_gaps.append(False)
    return row_gaps

def get_col_gaps(puzzle):
    col_gaps = [True for i in puzzle[0]]
    for row in puzzle:
        for i, character in enumerate(row):
            if character == '#':
                col_gaps[i] = False
    return col_gaps

def get_expanded_distance(coords1, coords2, row_gaps, col_gaps, factor=1):
    x_indices = range(min(coords1[0], coords2[0]), max(coords1[0], coords2[0]) + 1)
    y_indices = list(range(min(coords1[1], coords2[1]), max(coords1[1], coords2[1]) + 1))
    x_distance = -1
    for x_index in x_indices:
        if col_gaps[x_index]:
            x_distance += factor
        else:
            x_distance += 1
    y_distance = -1
    for y_index in y_indices:
        if row_gaps[y_index]:
            y_distance += factor
        else:
            y_distance += 1
    # print(f'gal1: {coords1}, gal2: {coords2}, row_gaps: {row_gaps}, col_gaps: {col_gaps}, distances: {x_distance}, {y_distance}')
    return x_distance + y_distance

def sum_expanded_distances(galaxies, row_gaps, col_gaps, factor=1):
    total = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            total += get_expanded_distance(galaxies[i], galaxies[j], row_gaps, col_gaps, factor)
    return total

def part2(filename):
    EXPANSION = 1_000_000
    puzzle = get_puzzle(filename)
    galaxies = get_galaxy_coords(puzzle)
    row_gaps = get_row_gaps(puzzle)
    col_gaps = get_col_gaps(puzzle)
    return sum_expanded_distances(galaxies, row_gaps, col_gaps, factor=EXPANSION)


if __name__ == '__main__':
    filename = 'input.txt'
    print(part_1(filename)) # 9639160
    print(part2(filename)) # 752936133304