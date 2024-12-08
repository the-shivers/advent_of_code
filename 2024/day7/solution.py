def recurse(target, total, nums, ops):
    if len(nums) == 0: 
        return total == target
    elif total > target: 
        return False
    else: 
        return any(
            [recurse(target, f(total, nums[0]), nums[1:], ops) for f in ops]
        )

if __name__ == '__main__':
    pt1 = pt2 = 0
    ops1 = (lambda x, y: x + y, lambda x, y: x * y)  # +, *
    ops2 = (*ops1, lambda x, y: int(str(x) + str(y)))  # +, *, ||

    with open('input.txt') as file:
        while line := file.readline():
            target_str, numbers_str = line.strip().split(': ')
            target = int(target_str)
            nums = [int(n) for n in numbers_str.split()]
            pt1 += target if recurse(target, nums[0], nums[1:], ops1) else 0
            pt2 += target if recurse(target, nums[0], nums[1:], ops2) else 0
            
    print(f'Part 1: {pt1}\nPart 2: {pt2}')