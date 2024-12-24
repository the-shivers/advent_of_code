from collections import deque

inputs = {}
combos = deque()
input_txt = 'input.txt'
with open(input_txt) as file:
    for line in file:
        if not line.strip():
            continue
        if ':' in line:
            k, v = line.strip().split(': ')
            inputs[k] = int(v)
        else:
            combos.append([i for i in line.strip().split(' ') if i != '->'])

def swap_outputs(combos, o1, o2):
    for combo1 in combos:
        if combo1[3] == o1:
            for combo2 in combos:
                if combo2[3] == o2:
                    combo1[3], combo2[3] = o2, o1
                    return combos
        elif combo1[3] == o2:
            for combo2 in combos:
                if combo2[3] == o1:
                    combo1[3], combo2[3] = o1, o2
                    return combos

def evaluate(input1, operator, input2):
    if operator == 'AND': return input1 and input2
    elif operator == 'OR': return input1 or input2
    elif operator == 'XOR': return input1 ^ input2

def fill_inputs(inputs, combos):
    while combos:
        curr = combos.pop()
        if curr[0] in inputs and curr[2] in inputs:
            inputs[curr[3]] = evaluate(inputs[curr[0]], curr[1], inputs[curr[2]])
        else:
            combos.appendleft(curr)
    return inputs

new_inputs = fill_inputs(inputs.copy(), combos.copy())
print("Part 1:", int(''.join(str(new_inputs[k]) for k in sorted((k for k in new_inputs if k.startswith('z')), reverse=True)), 2))

# Part 2
# Solved manually by examining input ¯\_(ツ)_/¯
combos = swap_outputs(combos, 'kth', 'z12')
combos = swap_outputs(combos, 'gsd', 'z26')
combos = swap_outputs(combos, 'z32', 'tbt')
combos = swap_outputs(combos, 'qnf', 'vpm')
new_inputs = fill_inputs(inputs, combos)

x_str = ''.join([str(new_inputs[k]) for k in sorted((k for k in new_inputs if k.startswith('x')), reverse=True)])
y_str = ''.join([str(new_inputs[k]) for k in sorted((k for k in new_inputs if k.startswith('y')), reverse=True)])
target = int(x_str, 2) + int(y_str, 2)
z_str = ''.join([str(new_inputs[k]) for k in sorted((k for k in new_inputs if k.startswith('z')), reverse=True)])
result = int(z_str, 2)
if result == target:
    print("Part 2:", ",".join(sorted(['kth', 'z12', 'gsd', 'z26', 'z32', 'tbt', 'qnf', 'vpm'])))