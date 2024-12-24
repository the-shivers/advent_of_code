from collections import deque

with open('input.txt') as f:
    vals, ops = f.read().strip().split('\n\n')
inputs = {k: int(v) for k, v in (l.split(': ') for l in vals.splitlines())}
combos = deque([[j for j in i.split() if j != '->'] for i in ops.splitlines()])

def swap_outputs(combos, o1, o2):
    idx1 = next((i for i, combo in enumerate(combos) if combo[3] == o1))
    idx2 = next((i for i, combo in enumerate(combos) if combo[3] == o2))
    combos[idx1][3], combos[idx2][3] = combos[idx2][3], combos[idx1][3]
    return combos

def evaluate(input1, operator, input2):
    if operator == 'AND': return input1 and input2
    elif operator == 'OR': return input1 or input2
    elif operator == 'XOR': return input1 ^ input2

def fill_inputs(inputs, combos):
    while combos:
        curr = combos.popleft()
        if curr[0] in inputs and curr[2] in inputs:
            inputs[curr[3]] = evaluate(inputs[curr[0]], curr[1], inputs[curr[2]])
        else:
            combos.append(curr)
    return inputs

new_inputs = fill_inputs(inputs.copy(), combos.copy())
z_outputs = {k: v for k, v in new_inputs.items() if k.startswith('z')}
binary = ''.join(str(z_outputs[k]) for k in sorted(z_outputs, reverse=True))
print("Part 1:", int(binary, 2))

# Part 2
# Solved manually by examining input ¯\_(ツ)_/¯
swaps = [('kth', 'z12'), ('gsd', 'z26'), ('z32', 'tbt'), ('qnf', 'vpm')]
for o1, o2 in swaps:
    combos = swap_outputs(combos, o1, o2)
new_inputs = fill_inputs(inputs, combos)

x_outputs = {k: v for k, v in new_inputs.items() if k.startswith('x')}
y_outputs = {k: v for k, v in new_inputs.items() if k.startswith('y')}
z_outputs = {k: v for k, v in new_inputs.items() if k.startswith('z')}

target = int(''.join(str(x_outputs[k]) for k in sorted(x_outputs, reverse=True)), 2) + \
         int(''.join(str(y_outputs[k]) for k in sorted(y_outputs, reverse=True)), 2)
result = int(''.join(str(z_outputs[k]) for k in sorted(z_outputs, reverse=True)), 2)

if result == target:
    print("Part 2:", ",".join(sorted(sum(swaps, ()))))