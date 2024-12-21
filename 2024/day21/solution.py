from functools import lru_cache 

KEY_ROWS = [
    [7, 8, 9],
    [4, 5, 6], 
    [1, 2, 3],
    ['', 0, 'A']
]

DIR_ROWS = [
    ['', '^', 'A'],
    ['<', 'v', '>']
]

@lru_cache(maxsize = None) 
def key_to_coords(k):
    if k == '':
        raise("Shouldn't be here!")
    elif k == 'A':
        return 2, 3
    for y, row in enumerate(KEY_ROWS):
        for x, num in enumerate(row):
            if int(k) == num:
                return x, y
            
@lru_cache(maxsize = None) 
def dir_to_coords(k):
    if k == '':
        raise("Shouldn't be here!")
    for y, row in enumerate(DIR_ROWS):
        for x, char in enumerate(row):
            if k == char:
                return x, y
            

# def keypad_instructions_dfs(code, pos, paths = []):
#     rx, ry = pos
#     if not code:
#         return paths
#     nx, ny = key_to_coords(code[0])
#     if rx < nx:
#         res = keypad_instructions_dfs(code, (rx+1, ry), ['>'] + paths)
#         paths.append()
#     if rx > nx:
#         paths.append(keypad_instructions_dfs(code, (rx-1, ry), ['<'] + paths))
#     if ry < ny:
#         paths.append(keypad_instructions_dfs(code, (rx, ry+1), ['v'] + paths))
#     if ry > ny:
#         paths.append(keypad_instructions_dfs(code, (rx, ry-1), ['^'] + paths))
#     if rx == nx and ry == ny:
#         paths.append(keypad_instructions_dfs(code[1:], (rx, ry), ['A'] + paths))
#     return paths
    


            

# +---+---+---+
# | 7 | 8 | 9 | 
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

def code_to_dirs(code):
    dirs = []
    rx, ry = (2, 3)
    while code:
        nx, ny = key_to_coords(code[0])
        if ny == 3:
            while rx < nx:
                dirs.append('>')
                rx += 1
            while rx > nx:
                dirs.append('<')
                rx -= 1
        elif nx == 0:
            while ry < ny:
                dirs.append('v')
                ry += 1
            while ry > ny:
                dirs.append('^')
                ry -= 1
        while rx < nx:
            dirs.append('>')
            rx += 1
        while rx > nx:
            dirs.append('<')
            rx -= 1
        while ry < ny:
            dirs.append('v')
            ry += 1
        while ry > ny:
            dirs.append('^')
            ry -= 1
        dirs.append('A')
        code = code[1:]
    return dirs

def dir_to_dirs(code):
    dirs = []
    rx, ry = (2, 0)
    while code:
        nx, ny = dir_to_coords(code[0])
        if ny == 0:
            while rx < nx:
                dirs.append('>')
                rx += 1
            while rx > nx:
                dirs.append('<')
                rx -= 1
        elif nx == 0:
            while ry < ny:
                dirs.append('v')
                ry += 1
            while ry > ny:
                dirs.append('^')
                ry -= 1
        while rx < nx:
            dirs.append('>')
            rx += 1
        while rx > nx:
            dirs.append('<')
            rx -= 1
        while ry < ny:
            dirs.append('v')
            ry += 1
        while ry > ny:
            dirs.append('^')
            ry -= 1
        dirs.append('A')
        code = code[1:]
    return dirs

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

input_txt = 'example.txt'
# input_txt = 'input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

pt1 = 0
for code in lines:
    a = code_to_dirs(code)
    b = dir_to_dirs(a)
    c = dir_to_dirs(b)
    print(code, '->', ''.join(c), len(c), 'int', int(code.split('A')[0]))
    pt1 += (len(c) * int(code.split('A')[0]))
print("Part 1:", pt1) 


# 230906 is too high


DIRS = {
    '^': (0, -1), 'v': (0, 1), 
    '<': (-1, 0), '>': (1, 0)
}

def compile(code, rows, pos):
    result = []
    for c in code:
        if c in DIRS:
            dx, dy = DIRS[c]
            pos = (pos[0]+dx, pos[1]+dy)
            # print(c, pos)
            continue
        result.append(rows[pos[1]][pos[0]])
    return ''.join(result)

a = compile('<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A', DIR_ROWS, (2, 0))
# <A>Av<<AA>^AA>AvAA^A<vAAA>^A
# <A>A v<<AA>^AA> AvAA^A<vAAA>^A

a = compile('v<<A>>^AvA^Av<<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^AA<A>Av<<A>A>^AAAvA<^A>A', DIR_ROWS, (2, 0))
# <A>A<AAv<AA>>^AvAA^A<vAAA>^A
# <A>A <AAv<AA>>^ AvAA^A<vAAA>^A

# a = compile('<A>Av<<AA>^AA>AvAA^A<vAAA>^A', KEY_ROWS, (2, 3))

a = compile('<A>Av<<AA>^AA>AvAA^A<vAAA>^A', DIR_ROWS, (2, 0))
# ^A<<^^A>>AvvvA
print(a)
a = compile('<A>A<AAv<AA>>^AvAA^A<vAAA>^A', DIR_ROWS, (2, 0))
# ^A^^<<A>>AvvvA
print(a)

# Official answer
# <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# <A>Av<<AA>^AA>AvAA^A<vAAA>^A
# ^A<<^^A>>AvvvA

# My answer
# v<<A>>^AvA^Av<<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^AA<A>Av<<A>A>^AAAvA<^A>A
# <A>A<AAv<AA>>^AvAA^A<vAAA>^A
# ^A^^<<A>>AvvvA

# Why does goign left first win on the official answer?
# <<^^A
# expands to v<<AA>^AA>A
# v<<AA>^AA>A
# expadns to 
# <vA <A A >>^A A vA <^A >A A vA ^A <vA

# vs

# ^^<<A
# expands to <AAv<AA>>^A
# <AAv<AA>>^A
# expands to
# v<<A >>^A A <vA <A >>^A A vA A <^A >A <vA