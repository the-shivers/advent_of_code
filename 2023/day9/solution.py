# filepath = 'example.txt'
filepath = 'input.txt'

# Part 1
def get_histories(filepath: str) -> list:
    """Returns a list of lists of integers representing oasis histories."""
    histories = []
    with open(filepath) as lines:
        for line in lines:
            histories.append(list(int(i) for i in line.strip().split()))
    return histories
    
def difference_history(history_list: list) -> list:
    """Given a list of integers, generates a differenced list."""
    return [history_list[i+1] - history_list[i] for i in range(len(history_list)-1)]

def check_all_zeroes(history_list: list) -> bool:
    """Based implicit type conversions"""
    return not any(history_list)

def reduce_history(history_list: list, max_depth: int = 100) -> list:
    """Reduces a history list by computing differences up to a maximum depth."""
    reduction_steps = [history_list]
    current_list = history_list
    for current_depth in range(max_depth):
        current_list = difference_history(current_list)
        reduction_steps.append(current_list)
        if check_all_zeroes(current_list):
            return reduction_steps
    raise ValueError("Failed to reduce to all zeroes within max depth")

def extrapolate(reduction_steps: list) -> list:
    """Returns extrapolated reduction steps (i.e. each step has an additional item). Doesn't sum."""
    rev = [i for i in reversed(reduction_steps)]
    for i, step in enumerate(rev):
        if i == 0:
            step.append(0)
            continue
        step.append(step[-1] + rev[i - 1][-1])
    return reduction_steps
        
def part_1(filepath: str) -> int:
    total = 0
    histories = get_histories(filepath)
    for history in histories:
        reduced = reduce_history(history)
        extrapolated = extrapolate(reduced)
        total += extrapolated[0][-1]
    return total

# Part 2
def reverse_extrapolate(reduction_steps: list) -> list:
    """Reverse extrapolate, adding zeroes to the beginning and figuring out numbers to create appropriate differences."""
    rev = [i for i in reversed(reduction_steps)]
    for i, step in enumerate(rev):
        if i == 0:
            # step.append(0)
            step.insert(0, 0)
            continue
        # step.append(step[-1] + rev[i - 1][-1])
        step.insert(0, step[0] - rev[i - 1][0])
    return reduction_steps

def part_2(filepath: str) -> int:
    total = 0
    histories = get_histories(filepath)
    for history in histories:
        reduced = reduce_history(history)
        extrapolated = reverse_extrapolate(reduced)
        total += extrapolated[0][0]
    return total

print(part_1(filepath))
print(part_2(filepath))