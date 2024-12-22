from functools import lru_cache

KEY_ROWS = (
    ('7', '8', '9'),
    ('4', '5', '6'), 
    ('1', '2', '3'),
    ('X', '0', 'A'),
)

DIR_ROWS = (
    ('X', '^', 'A'),
    ('<', 'v', '>'),
)

@lru_cache(maxsize = None) 
def key_to_pos(key_pad, key):
    """Essentially builds a key -> coords dict."""
    if key == '':
        raise("Shouldn't be here!")
    for y, row in enumerate(key_pad):
        for x, char in enumerate(row):
            if key == char:
                return x, y

@lru_cache(maxsize = None) 
def get_paths(
    keypad: tuple[tuple[str]], 
    start: tuple[int, int], 
    end: tuple[int, int],
    prepath: str = ''
) -> list[str]:
    sx, sy = start
    ex, ey = end
    paths = []
    if start == end:
        return [prepath]  # Return list containing the current path
    if ex > sx and keypad[sy][sx+1] != 'X':
        paths.extend(get_paths(keypad, (sx+1, sy), end, prepath + '>'))
    elif ex < sx and keypad[sy][sx-1] != 'X':
        paths.extend(get_paths(keypad, (sx-1, sy), end, prepath + '<'))
    if ey > sy and keypad[sy+1][sx] != 'X':
        paths.extend(get_paths(keypad, (sx, sy+1), end, prepath + 'v'))
    elif ey < sy and keypad[sy-1][sx] != 'X':
        paths.extend(get_paths(keypad, (sx, sy-1), end, prepath + '^'))
    return paths

@lru_cache(maxsize = None) 
def get_min_len(key_pad, code, robots):
    """Recursively returns the minimum length of a string."""
    if robots == 0:
        return len(code)
    current_position = key_to_pos(key_pad, 'A')
    minimal_length = 0
    for letter in code:
        seq_results = []
        for sequence in get_paths(key_pad, current_position, key_to_pos(key_pad, letter)):
            seq_results.append(get_min_len(DIR_ROWS, sequence  + 'A', robots - 1))
        minimal_length += min(seq_results)
        current_position = key_to_pos(key_pad, letter)
    return minimal_length

input_txt = 'input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

pt1 = pt2 = 0
for line in lines:
    pt1 += int(line[:-1]) * get_min_len(KEY_ROWS, line, 3)
    pt2 += int(line[:-1]) * get_min_len(KEY_ROWS, line, 26)
print(f"Part 1: {pt1}\nPart 2: {pt2}")