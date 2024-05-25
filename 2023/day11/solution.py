

def get_puzzle(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]
    
filename = 'example.txt'
puzzle = get_puzzle(filename)

def expand_rows(puzzle):
    new_puzzle = [] # To avoid modifying the original puzzle
    for row in puzzle:
        new_puzzle.append(str(row)) # Always add this
        if row.find('#') == -1:
            new_puzzle.append(str(row))
    return new_puzzle

def expand_cols(puzzle):
    # Loop through once to identify columns to expand
        
    # Loop through again to expand, a la expand_rows




print('\n'.join(puzzle))
new = expand_rows(puzzle)
print('\n'.join(new))