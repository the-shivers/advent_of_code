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

# Part 1
new_inputs = fill_inputs(inputs.copy(), combos.copy())
z_outputs = {k: v for k, v in new_inputs.items() if k.startswith('z')}
binary = ''.join(str(z_outputs[k]) for k in sorted(z_outputs, reverse=True))
print("Part 1:", int(binary, 2))

# Part 2
# (Solved manually by examining input ¯\_(ツ)_/¯)
swaps = [('kth', 'z12'), ('gsd', 'z26'), ('z32', 'tbt'), ('qnf', 'vpm')]
for o1, o2 in swaps:
    combos = swap_outputs(combos, o1, o2)
new_inputs = fill_inputs(inputs.copy(), combos.copy())

x_outputs = {k: v for k, v in new_inputs.items() if k.startswith('x')}
y_outputs = {k: v for k, v in new_inputs.items() if k.startswith('y')}
z_outputs = {k: v for k, v in new_inputs.items() if k.startswith('z')}

target = int(''.join(str(x_outputs[k]) for k in sorted(x_outputs, reverse=True)), 2) + \
         int(''.join(str(y_outputs[k]) for k in sorted(y_outputs, reverse=True)), 2)
result = int(''.join(str(z_outputs[k]) for k in sorted(z_outputs, reverse=True)), 2)

if result == target:
    print("Part 2:", ",".join(sorted(sum(swaps, ()))))


# New Part 2
class AdderCell:
    def __init__(self, i):
        self.i = i
        self.direct_compare = f"x{i:02d} XOR y{i:02d}"
        self.carry_and = f"x{i-1:02d} AND y{i-1:02d}" if i > 0 else None
        self.should_output = f"z{i:02d}"

def find_gate_for_output(combos, output):
    for combo in combos:
        if combo[3] == output:
            return combo
    return None

def trace_inputs(combos, output):
    gate = find_gate_for_output(combos, output)
    if not gate:
        return None
    
    result = {
        'output': output,
        'operation': gate[1],
        'inputs': [gate[0], gate[2]],
        'input_gates': []
    }
    
    for input_wire in [gate[0], gate[2]]:
        input_gate = find_gate_for_output(combos, input_wire)
        if input_gate:
            result['input_gates'].append(trace_inputs(combos, input_wire))
    
    return result

def print_gate_structure(gate, indent=0):
    if not gate:
        return
    print(" " * indent + f"{gate['output']}: {gate['operation']} ({', '.join(gate['inputs'])})")
    for input_gate in gate['input_gates']:
        print_gate_structure(input_gate, indent + 2)

def verify_adder_cell(gate_structure, expected):
    """Verify if a gate structure matches expected adder behavior"""
    # First check: top level should be XOR
    if gate_structure['operation'] != 'XOR':
        return False, f"Top gate should be XOR, got {gate_structure['operation']}"
    
    # Look for direct XOR of x and y bits in either input
    direct_xor = None
    for input_gate in gate_structure['input_gates']:
        if input_gate['operation'] == 'XOR':
            inputs = input_gate['inputs']
            # Check both orders: x,y and y,x
            if ((inputs[0].startswith('x') and inputs[1].startswith('y')) or
                (inputs[0].startswith('y') and inputs[1].startswith('x'))):
                direct_xor = input_gate
                break
    
    if not direct_xor:
        return False, f"No direct XOR comparison found in {gate_structure['inputs']}"
    
    # Verify bit position matches (handling both x,y and y,x order)
    x_bit = next(i for i in direct_xor['inputs'] if i.startswith('x'))
    if x_bit != f"x{expected.i:02d}":
        return False, f"Wrong bit position: {x_bit} vs expected x{expected.i:02d}"
    
    return True, "Valid adder cell"

# Test for z00 through z45
for i in range(46):
    print(f"\nAnalyzing z{i:02d}:")
    gate = trace_inputs(combos, f"z{i:02d}")
    if gate:
        # print_gate_structure(gate)
        valid, reason = verify_adder_cell(gate, AdderCell(i))
        print(f"Valid: {valid}, Reason: {reason}")