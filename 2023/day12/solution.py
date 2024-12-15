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
        # print(f'string {string} with int_list {int_list} had {len(solutions)} solutions.\n{solutions}\n')
    return pt_1_answer

print(verbose_solve('input.txt'))

# Part 2

# I may have made a huge mistake trying brute force. Let's just roll with it though and see what happens.

def unfold(string, int_tup):
    """We need int_tup to be a tuple, so that its hashable for our recursive solution."""
    string = (string + '?') * 5
    string = string[:-1]
    int_tup = int_tup * 5
    return string, tuple(int_tup)

# I am thinking of recursion with hash tables. I'm likely to encounter the 
# same substring / int groups # many times and I can save time by stashing 
# the solution to them.

# filename = 'input.txt'
# puzzle = get_puzzle(filename)
# string, int_tup = unfold(*puzzle[1])
# question_indices = [i for i, ltr in enumerate(string) if ltr == '?']
# q = len(question_indices)
# current_broken_parts = string.count('#')
# total_broken_parts = sum(int_tup)
# So total possibilities = total_broken_parts - current_broken_parts choose q e.g. 92k.

# '?###??????????###??????????###??????????###??????????###????????'
# [3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1]
# Answer: 506250

# '???#???.?#??????????#???.?#??????????#???.?#??????????#???.?#??????????#???.?#??????'
# [1, 2, 2, 3, 2, 1, 2, 2, 3, 2, 1, 2, 2, 3, 2, 1, 2, 2, 3, 2, 1, 2, 2, 3, 2]
# Answer: unknown
# Possibilities: 69 choose 40
# Over quintillion combinations lmaooooo

# Alright, I am throwing in the towel and looking at solutions others have developed.
# This superb writeup by @xavdid basically confirmed the approach I was going to go with
# (recursive + hashed), but helped me get unstuck. Apparently this is called "dynamic programming"
# which somehow I didn't know about, outside of toy examples e.g. fibonacci.
# https://advent-of-code.xavd.id/writeups/2023/day/12/

from functools import cache

@cache
def get_valid_solutions_count(string: str, int_tup: list[int]) -> int:
    # define base case
    if not string: # string == ''
        return len(int_tup) == 0 # bool, i.e. 1
        # since if no string left, we only succeed if no groups left
    if not int_tup: # int_tup == []
        return '#' not in string # bool, i.e. 1, 
        # since if no broken part groups remain in int_tup
        # we only get a success if remaining list is all '?' and '.'
    # Reduce remaining cases toward base case
    char, rem_string = string[0], string[1:]
    if char == '.':
        return get_valid_solutions_count(rem_string, int_tup)
    if char == '#':
        group = int_tup[0]
        # We're in the first grouping. It has to have exactly the right number of '#' and '?' to succeed.
        if (
            len(string) >= group # string must be long enough for whole group
            and all(i != '.' for i in string[:group]) # string must not contain '.'
            and (len(string) == group or string[group] != "#") # character after full 
            # group must not also be #, which indicates a failure (groups cannot touch)
        ):
            return get_valid_solutions_count(string[group + 1:], int_tup[1:])
        return 0 # failure if above requirements aren't met
    if char == '?': # sum case if . and case if #
        solutions_if_period = get_valid_solutions_count(f".{rem_string}", int_tup)
        solutions_if_pound = get_valid_solutions_count(f"#{rem_string}", int_tup)
        return solutions_if_period + solutions_if_pound
    
def solve_pt_2(filename):
    puzzle = get_puzzle(filename)
    total = 0
    for string, int_tup in puzzle:
        string, int_tup = unfold(string, int_tup)
        total += get_valid_solutions_count(string, int_tup)
    return total

print(solve_pt_2('input.txt')) # 8475948826693

from functools import cache

def parse_line(line):
    pattern, numbers = line.split()
    numbers = tuple(map(int, numbers.split(',')))
    return pattern, numbers

def solve_line(pattern, numbers):
    @cache
    def dp(pos, current_group, group_index):
        # Base case: reached end of pattern
        if pos == len(pattern):
            # Valid if we've used all groups and aren't in middle of group
            if group_index == len(numbers) and current_group == 0:
                return 1
            # Also valid if we're on last group and have completed it
            if group_index == len(numbers) - 1 and current_group == numbers[group_index]:
                return 1
            return 0
        
        result = 0
        for char in ['#', '.'] if pattern[pos] == '?' else pattern[pos]:
            if char == '#':
                # Continue or start damaged group
                result += dp(pos + 1, current_group + 1, group_index)
            else:  # char == '.'
                if current_group == 0:
                    # No group in progress, just move forward
                    result += dp(pos + 1, 0, group_index)
                elif group_index < len(numbers) and current_group == numbers[group_index]:
                    # Successfully completed a group
                    result += dp(pos + 1, 0, group_index + 1)
            
        return result

    return dp(0, 0, 0)

def solve_part1(input_lines):
    total = 0
    for line in input_lines:
        if not line.strip():
            continue
        pattern, numbers = parse_line(line)
        arrangements = solve_line(pattern, numbers)
        total += arrangements
    return total

# Read from input.txt
with open('input.txt', 'r') as f:
    input_lines = f.readlines()

result = solve_part1(input_lines)
print(f"Part 1 result: {result}")  # Should print 6852


from functools import cache

def parse_line(line, unfold=False):
    pattern, numbers = line.split()
    numbers = tuple(map(int, numbers.split(',')))
    
    if unfold:
        pattern = '?'.join([pattern] * 5)
        numbers = numbers * 5
        
    return pattern, numbers

def solve_line(pattern, numbers):
    @cache
    def dp(pos, current_group, group_index):
        # Base case: reached end of pattern
        if pos == len(pattern):
            if group_index == len(numbers) and current_group == 0:
                return 1
            if group_index == len(numbers) - 1 and current_group == numbers[group_index]:
                return 1
            return 0
        
        # Early termination checks
        if group_index < len(numbers) and current_group > numbers[group_index]:
            return 0
        
        result = 0
        current_char = pattern[pos]
        
        if current_char in '.?':
            if current_group == 0:
                # No group in progress, just move forward
                result += dp(pos + 1, 0, group_index)
            elif group_index < len(numbers) and current_group == numbers[group_index]:
                # Successfully completed a group
                result += dp(pos + 1, 0, group_index + 1)
                
        if current_char in '#?':
            # Can only continue/start group if we haven't exceeded total groups
            if group_index < len(numbers):
                result += dp(pos + 1, current_group + 1, group_index)
            
        return result

    return dp(0, 0, 0)

def solve_parts(input_lines):
    # Test individual lines first
    debug = False
    if debug:
        for line in input_lines:
            if not line.strip():
                continue
            pattern, numbers = parse_line(line, unfold=True)
            arrangements = solve_line(pattern, numbers)
            print(f"Line: {line.strip()} -> {arrangements} arrangements")
    
    # Solve both parts
    part1 = sum(solve_line(*parse_line(line)) for line in input_lines if line.strip())
    part2 = sum(solve_line(*parse_line(line, unfold=True)) for line in input_lines if line.strip())
    
    return part1, part2

# Verify with example input first
test_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()

test_part1, test_part2 = solve_parts(test_input)
print(f"Test Part 1: {test_part1}")  # Should be 21
print(f"Test Part 2: {test_part2}")  # Should be 525152

# Now solve the actual input
with open('input.txt', 'r') as f:
    input_lines = f.readlines()

part1, part2 = solve_parts(input_lines)
print(f"\nPart 1 result: {part1}")  # Should be 6852
print(f"Part 2 result: {part2}")  # Should be 8475948826693