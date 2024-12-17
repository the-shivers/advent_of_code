def get_val(state, v):
    """For getting combo operand values."""
    if v == 4: return state['A']
    elif v == 5: return state['B']
    elif v == 6: return state['C']
    else: return v

def run(state):
    """Run program to completion."""
    while state['pos'] < len(state['P']):
        op = state['P'][state['pos']]
        val = state['P'][state['pos'] + 1]
        if op == 0: # adv
            state['A'] //= 2 ** get_val(state, val)
        elif op == 1: # bxl
            state['B'] ^= val
        elif op == 2: # bst
            state['B'] = get_val(state, val) % 8
        elif op == 3: # jnz
            if state['A'] != 0:
                state['pos'] = val
                continue # no increment
        elif op == 4: # bxc
            state['B'] ^= state['C']
        elif op == 5: # out
            state['O'].append(get_val(state, val) % 8)
        elif op == 6: # bdv
            state['B'] = state['A'] // (2 ** get_val(state, val))
        elif op == 7: # cdv
            state['C'] = state['A'] // (2 ** get_val(state, val))
        state['pos'] += 2
    return state['O']

def dfs(program, acc, pos):
    """
    Find self-replicating program:
      1. Starting from rightmost target digit, increment A by up to 7.
      2. Once digit matches, multiply A by 8 to get new digit
      3. Repeat, backtracking if necessary.
    """
    for i in range(8):
        val = acc + i
        state = {'A': val, 'B': 0, 'C': 0, 'P': program, 'pos': 0, 'O': []}
        if run(state) == program[pos:]:
            if pos == 0:
                return val
            result = dfs(program, val * 8, pos - 1)
            if result:
                return result
    return None

with open('input.txt') as f:
    lines = f.readlines()
    state = {
        'A': int(lines[0].split(': ')[1]),
        'B': int(lines[1].split(': ')[1]),
        'C': int(lines[2].split(': ')[1]),
        'P': [int(x) for x in lines[4].split(': ')[1].split(',')],
        'pos': 0,
        'O': []
    }

# Part 1
print("Part 1:", ",".join(map(str, run(state))))

# Part 2
print("Part 2:", dfs(state['P'], 0, len(state['P']) - 1))