import itertools

def get_puzzle(filename):
    with open(filename) as lines:
        puzzle = []
        for line in lines:
            line = line.strip()
            string, int_list = line.split(' ')
            int_list = [int(i) for i in int_list.split(',')]
            puzzle.append((string, int_list))
        return puzzle

def count_broken_segments(string):
    return [len(substr) for substr in string.split('.') if len(substr) > 0]

def evaluate_solution(string, int_list):
    """Determines if string of parts matches int_list"""
    assert len(string.replace(".","").replace("#","")) == 0
    assert len(string) > 0
    return count_broken_segments(string) == int_list

def generate_brute_force_list(string, int_list):
    """given string full of ?s generates brute force solution list.
    Okay, we need to think about this more. The total number of broken parts always
    equals the sum of the elements of the broken segments list. Lets say its [1, 2, 2].
    This is 5 broken parts. They must be distributed over the question mark slots. So
    we get the indices of the question marks. And find combinations of those of 
    length sum(broken segments list).
    
    Long story short:
    its num_question_marks CHOOSE sum(int_list) combinations, not 2^num_question_marks!
    """
    brute_force_list = []
    question_indices = [i for i, ltr in enumerate(string) if ltr == '?']
    combos = list(itertools.combinations(question_indices, sum(int_list) - string.count('#')))
    for combo in combos:
        str_list = list(string) # Need to make it mutable
        for index in combo:
            str_list[index] = '#'
        brute_force_list.append(''.join(str_list).replace('?', '.')) # Replace remaining parts
    return brute_force_list

def get_solutions(string_list, int_list):
    solutions = []
    for string in string_list:
        if evaluate_solution(string, int_list):
            solutions.append(string)
    return solutions

def verbose_solve(filename):
    puzzle=get_puzzle(filename)
    pt_1_answer = 0
    for string, int_list in puzzle:
        possibilities = generate_brute_force_list(string, int_list)
        solutions = get_solutions(possibilities, int_list)
        pt_1_answer += len(solutions)
        print(f'string {string} with int_list {int_list} had {len(solutions)} solutions.\n{solutions}\n')
    return pt_1_answer

print(verbose_solve('input.txt'))

# Part 2

# I may have made a huge mistake. Let's just roll with it though and see what happens.

def unfold(string, int_list):
    string = (string + '?') * 5
    string = string[:-1]
    int_list = int_list * 5
    return string, int_list

def verbose_solve2(filename):
    puzzle=get_puzzle(filename)
    pt_1_answer = 0
    for string, int_list in puzzle:
        string, int_list = unfold(string, int_list)
        possibilities = generate_brute_force_list(string, int_list)
        solutions = get_solutions(possibilities, int_list)
        pt_1_answer += len(solutions)
        print(f'string {string} with int_list {int_list} had {len(solutions)} solutions.\n{solutions}\n')
    return pt_1_answer

print(verbose_solve2('example.txt')) # Times out. :(

# I am thinking of recursion with hash tables. I'm likely to encounter the 
# same substring / int groups # many times and I can save time by stashing 
# the solution to them.

filename = 'input.txt'
puzzle = get_puzzle(filename)
string, int_list = unfold(*puzzle[1])
question_indices = [i for i, ltr in enumerate(string) if ltr == '?']
q = len(question_indices)
current_broken_parts = string.count('#')
total_broken_parts = sum(int_list)
# So total possibilities = total_broken_parts - current_broken_parts choose q e.g. 92k.

# '?###??????????###??????????###??????????###??????????###????????'
# [3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1]
# Answer: 506250

# '???#???.?#??????????#???.?#??????????#???.?#??????????#???.?#??????????#???.?#??????'
# [1, 2, 2, 3, 2, 1, 2, 2, 3, 2, 1, 2, 2, 3, 2, 1, 2, 2, 3, 2, 1, 2, 2, 3, 2]
# Answer: unknown
# Possibilities: 69 choose 40
# Over quintillion combinations lmao









