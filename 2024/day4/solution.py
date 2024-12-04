# input_txt = 'advent_of_code/2024/day4/example.txt'
input_txt = 'advent_of_code/2024/day4/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

dirs = {
    "u": (0, -1), # up
    "ur": (1, -1), # up right
    "r": (1, 0), # right
    "dr": (1, 1), # down right
    "d": (0, 1), # etc.
    "dl": (-1, 1),
    "l": (-1, 0),
    "ul": (-1, -1)
}
diags = {k: v for k, v in dirs.items() if len(k) == 2}
one_dir = {"u": (0, -1)}
    
def word_search(
    pat: str, 
    grid: list[list[str]], 
    dirs: dict[str, tuple[int, int]]
) -> set[tuple[tuple[int, int], str]]:
    height, width = len(grid), len(grid[0])
    results = set()
    for start_y in range(height):
        for start_x in range(width):
            if grid[start_y][start_x] != pat[0]:
                continue
            for dir_str, (dx, dy) in dirs.items():
                for i, letter in enumerate(pat):
                    x = start_x + i * dx
                    y = start_y + i * dy
                    if (
                        x < 0 or x >= width or 
                        y < 0 or y >= height or 
                        grid[y][x] != letter
                    ):
                        break
                    if i == len(pat) - 1:
                        results.add(((start_x, start_y), dir_str))
    return results


# Part 1
print("Part 1:", len(word_search('XMAS', lines, dirs)))

# Part 2
counter = 0
a_coords = word_search('A', lines, one_dir)

for (x, y), _ in a_coords:
    if 1 <= x < len(lines[0]) - 1 and 1 <= y < len(lines) - 1: # avoid edges
        subgrid = [line[x - 1:x + 2] for line in lines[y - 1:y + 2]]
        counter += 1 if len(word_search('MAS', subgrid, diags)) == 2 else 0

print("Part 2:", counter)
