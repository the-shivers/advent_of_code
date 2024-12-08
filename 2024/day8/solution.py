from collections import defaultdict
from itertools import combinations

def load_data(filename='input.txt'):
    antennae = defaultdict(list)
    with open(filename) as f:
        lines = f.readlines()
        for y, line in enumerate(lines):
            for x, chr in enumerate(line.strip()):
                if chr != '.':
                    antennae[chr].append((x, y))
    return antennae, len(lines[0].strip()), len(lines) # dict, width, height

def extrapolate(start, delta, bounds):
    (x, y), (dx, dy) = start, delta
    points = set()
    while 0 <= x < bounds[0] and 0 <= y < bounds[1]:
        points.add((x, y))
        x, y = x + dx, y + dy
    return points

def solve():
    antennae, w, h = load_data()
    pt1, pt2 = set(), set()
    for ants in antennae.values():
        for (x1, y1), (x2, y2) in combinations(ants, 2):
            d = (x2 - x1, y2 - y1)
            candidates = {(x1 - d[0], y1 - d[1]), (x2 + d[0], y2 + d[1])}
            pt1.update(p for p in candidates if 0 <= p[0] < w and 0 <= p[1] < h)
            pt2.update(
                [(x1, y1), (x2, y2)],
                extrapolate((x1 - d[0], y1 - d[1]), (-d[0], -d[1]), (w, h)),
                extrapolate((x2 + d[0], y2 + d[1]), d, (w, h))
            )
    print(f"Part 1: {len(pt1)}")
    print(f"Part 2: {len(pt2)}")

if __name__ == '__main__':
    solve()