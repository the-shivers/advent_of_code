# input_txt = 'example.txt'
input_txt = 'input.txt'
with open(input_txt) as file:
    answers = []
    for line in file:
        l, r = line.split(': ')
        nums = [int(num) for num in r.strip().split()]
        answers.append((int(l.strip()), tuple(nums)))

def get_bin_list(num: int) -> list[int]:
    binary_str = str(bin(num)).split('0b')[1]
    return [int(i) for i in binary_str]

def get_tri_list(num: int) -> list[int]:
    if num == 0:
        return [0]
    nums = []
    while num:
        num, r = divmod(num, 3)
        nums.append(r)
    return nums[::-1]

def get_sign_permutations(i, base):
    keys = '+*|'
    perms = {0: []}
    for i in range(1, i):
        perms[i] = []
        for j in range(base**i): # generation
            bin_list = get_bin_list(j) if base == 2 else get_tri_list(j)
            indices = [0] * (i - len(bin_list)) + bin_list
            perms[len(indices)].append([keys[i] for i in indices])
    return perms

def evaluate_line(nums, signs):
    total = nums[0]
    for i, sign in enumerate(signs):
        if sign == '+':
            total += nums[i + 1]
        elif sign == '|':
            total = int(str(total) + str(nums[i + 1]))
        else:
            total *= nums[i + 1]
    return total

def solve(answers, perms):
    total = 0
    for answer, nums in answers:
        for perm in perms[len(nums) - 1]:
            if evaluate_line(nums, perm) == answer:
                total += answer
                break
    return total


# Part 1
perms = get_sign_permutations(12, 2)
print("Part 1:", solve(answers, perms))

# Part 2:
perms = get_sign_permutations(12, 3)
print("Part 2:", solve(answers, perms))