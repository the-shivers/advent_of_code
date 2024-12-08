input_txt = 'input.txt'
with open(input_txt) as file:
    answers = []
    for line in file:
        l, r = line.split(': ')
        nums = [int(num) for num in r.strip().split()]
        answers.append((int(l.strip()), tuple(nums)))

def add(n1, n2): return n1 + n2
def mult(n1, n2): return n1 * n2
def concat(n1, n2): return int(str(n1) + str(n2))

def recurse(target, total, nums):
    if len(nums) == 0:
        return total == target
    elif total > target:
        return False
    else:
        return any([recurse(target, f(total, nums[0]), nums[1:]) for f in funcs])

funcs = (add, mult)
print('Part 1:', sum(a[0] if recurse(a[0], a[1][0], a[1][1:]) else 0 for a in answers))

funcs = (add, mult, concat)
print('Part 2:', sum(a[0] if recurse(a[0], a[1][0], a[1][1:]) else 0 for a in answers))


