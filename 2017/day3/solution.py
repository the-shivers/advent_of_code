# These answers stolen from reddit thread:
# https://www.reddit.com/r/adventofcode/comments/7h7ufl/2017_day_3_solutions/

from itertools import count
from collections import defaultdict

n = 361527

# Part 1
i = 1
while i*i < n:
    i += 2
pivots = [i*i - k*(i-1) for k in range(4)]
for p in pivots:
    dist = abs(p - n)
    if dist <= (i-1)//2:
        print(i-1-dist)
        break

def sum_spiral():
    a, i, j = defaultdict(int), 0, 0
    a[0,0] = 1
    sn = lambda i,j: sum(a[k,l] for k in range(i-1,i+2)
                                for l in range(j-1,j+2))
    for s in count(1, 2):
        for _ in range(s):   i += 1; a[i,j] = sn(i,j); yield a[i,j]
        for _ in range(s):   j -= 1; a[i,j] = sn(i,j); yield a[i,j]
        for _ in range(s+1): i -= 1; a[i,j] = sn(i,j); yield a[i,j]
        for _ in range(s+1): j += 1; a[i,j] = sn(i,j); yield a[i,j]

def part2(n):
    for x in sum_spiral():
        if x>n: return x

print(part2(n))