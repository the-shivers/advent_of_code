# input_txt = 'example.txt'
input_txt = 'input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

# Part 1
acc = 0
pos = 0
visited = set()
while True:
    if pos in visited:
        break
    else:
        visited.add(pos)
    current = lines[pos]
    if current[0:3] == 'nop':
        pos += 1
    elif current[0:3] == 'acc':
        acc += int(current.split(' ')[1])
        pos += 1
    elif current[0:3] == 'jmp':
        pos += int(current.split(' ')[1])
    
print("Part 1:", acc)

# Part 2
# Brute force would be totally viable here (n^2)
# But maybe we can do better.
# Suppose we have dictionaries indicating the "what this leads to" and "what leads to this"
# From here we could work backwards...

# Or maybe we should think about this as a decision tree. 
# Every time we hit a nop or jmp we split and explore both paths. 
# Hm... but we can do better than this too. There are going to be subproblems.
# Or are there?
# Maybe we can do some small optimizations. If the redirect sends us to a node we already visited... then it's obviously no good.
# Okay, this sounds like a good strategy. The set essentially saves us from a lot of work. 

# import sys
# sys.setrecursionlimit(10000)

# def recurse(acc, pos, visited, flips_remaining):
#     print('pos', pos, 'acc', acc, 'flips', flips_remaining, lines[pos])
#     if pos in visited:
#         return (False, acc)
#     elif pos == len(lines) - 1:
#         return (True, acc)
#     visited.add(pos)
#     current = lines[pos]
#     res1, res2 = (False, 0), (False, 0)
#     if current[0:3] == 'acc':
#         res1 = recurse(acc + int(current.split(' ')[1]), pos + 1, visited, flips_remaining)
#     elif current[0:3] == 'jmp':
#         if flips_remaining > 0: 
#             res1 = recurse(acc, pos + 1, visited, flips_remaining - 1) # treat as nop
#         res2 = recurse(acc, pos + int(current.split(' ')[1]), visited, flips_remaining) # still treat as jmp
#     elif current[0:3] == 'nop':
#         if flips_remaining > 0: 
#             res1 = recurse(acc, pos + int(current.split(' ')[1]), visited, flips_remaining - 1) # treat as jmp
#         res2 = recurse(acc, pos + 1, visited, flips_remaining) # still treat as nop
#     if res1[0]:
#         return res1
#     else:
#         return res2

# acc = 0
# pos = 0
# visited = set()
# recurse(acc, pos, visited, 1)


# from collections import deque


# So which increment actually gets us to the last line? 
# Okay new approach, let's build double dictionaries (like we did last time). 
# Then we can solve the maze backwards.
# We will simply identify which paths could possibly (flipped or not) lead to the last space
# Then find the paths that could lead to that. 
# And so on and so forth.
# Wait this is retarded, it's literally the same problem. 
# Let's just get the BROOT done for now. 


def solve(lines):
    visited = set()
    acc = 0
    pos = 0
    while True:
        if pos in visited:
            return (False, acc)
        else:
            visited.add(pos)
        if pos == len(lines) - 1:
            return (True, acc)
        current = lines[pos]
        if current[0:3] == 'nop':
            pos += 1
        elif current[0:3] == 'acc':
            acc += int(current.split(' ')[1])
            pos += 1
        elif current[0:3] == 'jmp':
            pos += int(current.split(' ')[1])

for i in range(len(lines)):
    result = (False, 0)
    if lines[i][0:3] == 'jmp':
        new_lines = lines[:]
        new_lines[i] = 'nop ' + lines[i].split(' ')[1]
        result = solve(new_lines)
    elif lines[i][0:3] == 'nop':
        new_lines = lines[:]
        new_lines[i] = 'jmp ' + lines[i].split(' ')[1]
        result = solve(new_lines)
    if result[0]:
        print("Part 2:", result[1])



# ChatGPT version
def run(code, flip=None):
    acc = pos = 0
    seen = set()
    while pos not in seen and pos < len(code):
        seen.add(pos)
        op, val = code[pos].split(); val = int(val)
        if pos == flip:
            op = 'nop' if op == 'jmp' else 'jmp'

        if op == 'acc':
            acc += val; pos += 1
        elif op == 'jmp':
            pos += val
        else:                     # nop
            pos += 1
    return pos == len(code), acc

# ---------- pre-work ----------
ops, arg = zip(*(l.split() for l in lines))
arg = list(map(int, arg))
n = len(lines)

succ = [i + (arg[i] if ops[i] == 'jmp' else 1) for i in range(n)]

rev = [[] for _ in range(n + 1)]
for i, j in enumerate(succ):
    if 0 <= j <= n:
        rev[j].append(i)

can_exit = [False]*(n + 1)
stack = [n]
while stack:
    j = stack.pop()
    if can_exit[j]:
        continue
    can_exit[j] = True
    stack.extend(rev[j])

# ---------- find the flip ----------
pos = 0
seen = set()
flip_at = None
while pos not in seen:
    seen.add(pos)
    if ops[pos] == 'nop' and can_exit[pos + arg[pos]]:
        flip_at = pos; break
    if ops[pos] == 'jmp' and can_exit[pos + 1]:
        flip_at = pos; break
    pos += arg[pos] if ops[pos] == 'jmp' else 1

# ---------- final run ----------
_, accumulator = run(lines, flip=flip_at)
print(accumulator)      # → 1149