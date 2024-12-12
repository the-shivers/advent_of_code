with open('input.txt') as file:
    stones = [int(i) for i in file.readline().split()]

def get_distinct_stone_values(stone, cache):
    if stone not in cache:
        cache[stone] = {}
        if stone == 0:
            get_distinct_stone_values(1, cache)
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            half = len(s) // 2
            left = int(s[:half])
            right = int(s[half:])
            get_distinct_stone_values(left, cache)
            get_distinct_stone_values(right, cache)
        else:
            get_distinct_stone_values(stone * 2024, cache)

cache = {}
for stone in stones:
    get_distinct_stone_values(stone, cache)

for stone in cache:
    cache[stone][0] = 1

for blink in range(1, 75 + 1):
    for stone in cache: 
        if stone == 0:
            cache[stone][blink] = cache[1][blink - 1]
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            half = len(s) // 2
            l, r = int(s[:half]), int(s[half:])
            cache[stone][blink] = cache[l][blink - 1] + cache[r][blink - 1]
        else:
            cache[stone][blink] = cache[stone * 2024][blink - 1]

pt1 = pt2 = 0
for stone in stones:
    pt1 += cache[stone][25]
    pt2 += cache[stone][75]
print(f"Part 1: {pt1}\nPart 2: {pt2}")


