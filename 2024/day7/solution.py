def validate(target, nums, allow_concat=False):
    if len(nums) == 1: return target == nums[0]
    if nums[-1] > target: return False
    # Multiplication Case
    if target % nums[-1] == 0:
        if validate(target // nums[-1], nums[:-1], allow_concat):
            return True
    # Concatenation Case
    if allow_concat:
        digit_count = len(str(nums[-1]))
        if target % (10 ** digit_count) == nums[-1]:
            if validate(target // (10 ** digit_count), nums[:-1], allow_concat):
                return True
    # Addition Case
    return validate(target - nums[-1], nums[:-1], allow_concat)

def solve_puzzle(filename: str) -> tuple[int, int]:
    part1 = part2 = 0
    with open(filename) as file:
        for line in file:
            target_str, numbers_str = line.strip().split(': ')
            target = int(target_str)
            nums = [int(n) for n in numbers_str.split()]
            if validate(target, nums, False):
                part1 += target
            if validate(target, nums, True):
                part2 += target
    return part1, part2

if __name__ == '__main__':
    pt1, pt2 = solve_puzzle('input.txt')
    print(f'Part 1: {pt1}')
    print(f'Part 2: {pt2}')