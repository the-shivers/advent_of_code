from collections import deque

def get_next_secret(s):
    s = (s ^ (s * 64)) % 16777216
    s = (s ^ (s // 32)) % 16777216
    s = (s ^ (s * 2048)) % 16777216
    return s

with open('input.txt') as f:
    nums = [int(x) for x in f]

pt1, patterns = 0, {}
for secret in nums:
    diffs = deque(maxlen=4)
    seen = set()
    curr_secret = secret
    for _ in range(2000):
        prev_digit = curr_secret % 10
        curr_secret = get_next_secret(curr_secret)
        diffs.append(curr_secret % 10 - prev_digit)
        if len(diffs) == 4:
            diff_pattern = tuple(diffs)
            if diff_pattern not in seen:
                seen.add(diff_pattern)
                patterns[diff_pattern] = patterns.get(diff_pattern, 0) + curr_secret % 10
    pt1 += curr_secret

print(f"Part 1: {pt1}")
print(f"Part 2: {max(patterns.values())}")