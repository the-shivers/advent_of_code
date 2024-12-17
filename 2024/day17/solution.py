# OPCODES
def adv(d, combo_operand):
    op = c2l(d, combo_operand)
    d['A'] = d['A'] // (2 ** op)
    d['pos'] += 2

def bxl(d, literal_operand):
    d['B'] = d['B'] ^ literal_operand # May need to make trinary friendly
    d['pos'] += 2

def bst(d, combo_operand):
    op = c2l(d, combo_operand)
    d['B'] = op % 8
    d['pos'] += 2

def jnz(d, literal_operand):
    if d['A'] == 0:
        d['pos'] += 2
    else:
        d['pos'] = literal_operand

def bxc(d, ignored_operand):
    d['B'] = d['B'] ^ d['C']
    d['pos'] += 2

def out(d, combo_operand):
    op = c2l(d, combo_operand)
    d['pos'] += 2
    return op % 8

def bdv(d, combo_operand):
    op = c2l(d, combo_operand)
    d['B'] = d['A'] // (2 ** op)
    d['pos'] += 2

def cdv(d, combo_operand):
    op = c2l(d, combo_operand)
    d['C'] = d['A'] // (2 ** op)
    d['pos'] += 2

def c2l(d, op):
    if op == 4: return d['A']
    elif op == 5: return d['B']
    elif op == 6: return d['C']
    return op

opcodes = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}

def run(d):
    f = opcodes[d['P'][d['pos']]]
    op = d['P'][d['pos'] + 1]
    res = f(d, op)
    if res is not None:
        d['O'].append(res)

def test():
    # If register C contains 9, the program 2,6 would set register B to 1.
    d = {'A': 0, 'B': 0, 'C': 9, 'P': [2, 6], 'pos': 0, 'O': []}
    run(d)
    assert d['B'] == 1
    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    d = {'A': 10, 'B': 0, 'C': 0, 'P': [5,0,5,1,5,4], 'pos': 0, 'O': []}
    run(d)
    run(d)
    run(d)
    assert d['O'] == [0, 1, 2]
    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    d = {'A': 2024, 'B': 0, 'C': 0, 'P': [0,1,5,4,3,0], 'pos': 0, 'O': []}
    output = []
    while d['pos'] < len(d['P']):
        run(d)
    assert d['O'] == [4,2,5,6,7,7,7,7,3,1,0]
    # If register B contains 29, the program 1,7 would set register B to 26.
    d = {'A': 2024, 'B': 29, 'C': 0, 'P': [1, 7], 'pos': 0}
    run(d)
    assert d['B'] == 26
    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    d = {'A': 2024, 'B': 2024, 'C': 43690, 'P': [4, 0], 'pos': 0}
    run(d)
    assert d['B'] == 44354
    # Actual example
    d = {"A": 729, "B": 0, "C": 0, "P": [0,1,5,4,3,0], 'pos': 0, "O": []}
    while d['pos'] < len(d['P']):
        run(d)
    assert d['O'] == [4,6,3,5,6,3,5,2,1,0]
    # Part 2
    d = {"A": 117440, "B": 0, "C": 0, "P": [0,3,5,4,3,0], "pos": 0, "O": []}
    while d['pos'] < len(d['P']):
        run(d)
    assert d['O'] == d['P']


test()  

def get_output(d):
    while d['pos'] < len(d['P']):
        run(d)
    return d['O']

input_txt = 'input.txt'
d = {}
with open(input_txt) as file:
    for line in file:
        if 'A' in line:
            d['A'] = int(line.strip().split(': ')[-1])
        elif 'B' in line:
            d['B'] = int(line.strip().split(': ')[-1])
        elif 'C' in line:
            d['C'] = int(line.strip().split(': ')[-1])
        elif 'P' in line:
            d['P'] = [int(i) for i in line.strip().split(': ')[-1].split(',')]
d['pos'] = 0
d['O'] = []

# Part 1
while d['pos'] < len(d['P']):
    run(d)
print("Part 1:", ",".join(str(i) for i in d['O']))

# Part 2
# Manipulating the ones digit (adding 0 to 8) influences the leftmost digit.
# Multiplying by 8 adds another digit on the left.
# Algorithm: increment by up to 8 until we have a match, then multiply by 8 and repeat.
# Sometimes we will have to backtrack--DFS should take care of this. 

# 3             =                  0 # Correct
# 8 * 3         =                3,0 # Correct
# 8 * 8 * 3     =              5,3,0 # Correct
# 8*8*8*3       =            3,5,3,0 # Wrong, should be 5,5,3,0
# 8*8*8*3+2     =            5,5,3,0 # Correct, next we need 2
# (8*8*8*3+2)*8 =          3,5,5,3,0 # Wrong, we need 2!
# (8*8*8*3+2)*8+1 etc.


def dfs(d, so_far, pos):
    d = d.copy()
    for i in range(8):
        d['B'] = 0
        d['C'] = 0
        d['pos'] = 0
        d['O'] = []
        d['A'] = so_far + i
        solution = get_output(d.copy())
        if solution == d['P'][pos:]:
            if pos == 0:
                return so_far + i
            recursive_result = dfs(d, (so_far + i) * 8, pos - 1)
            if recursive_result != 0:  # If the recursive call found a solution
                return recursive_result    
    return 0


pt2 = dfs(d, 0, len(d['P']) - 1)
print("Part 2:", pt2)