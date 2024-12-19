from functools import lru_cache

@lru_cache(maxsize=None)
def get_combos(s, nums):
    # Base case
    if not s: return 1 if not nums else 0
    # Recursive cases
    if s[0] == '.': return get_combos(s[1:], nums)
    if s[0] == '?': return get_combos('.' + s[1:], nums) + get_combos('#' + s[1:], nums)
    # Obstacle (#) cases
    if not nums: return 0
    if len(s) < nums[0]: return 0
    if any(c == '.' for c in s[:nums[0]]): return 0
    if len(s) == nums[0]: return 0 if len(nums) > 1 else 1
    if s[nums[0]] == '#': return 0
    return get_combos(s[nums[0] + 1:], nums[1:])

def parse_input(filename):
    with open(filename) as f:
        return [(s, tuple(map(int, n.split(',')))) for s, n in 
               (line.strip().split() for line in f)]

def unfold(s, nums):
    return '?'.join([s] * 5), nums * 5

puzzles = parse_input('input.txt')
print("Part 1:", sum(get_combos(*p) for p in puzzles))
print("Part 2:", sum(get_combos(*unfold(*p)) for p in puzzles))