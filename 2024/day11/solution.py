from functools import lru_cache

with open('input.txt') as file:
    stones = [int(i) for i in file.readline().split()]

@lru_cache(maxsize=None)
def quick_blink(stone, num_blinks):
    if num_blinks == 0:
        return 1
    if stone == 0:
        return quick_blink(stone + 1, num_blinks - 1)
    elif len(str(stone)) % 2 == 0:
        return (
            quick_blink(int(str(stone)[:len(str(stone)) // 2]), num_blinks - 1) + 
            quick_blink(int(str(stone)[len(str(stone)) // 2:]), num_blinks - 1)
        )
    else:
        return quick_blink(stone * 2024, num_blinks - 1)

pt1 = pt2 = 0
for stone in stones:
    pt1 += quick_blink(stone, 25)
    pt2 += quick_blink(stone, 75)
print(f"Part 1: {pt1}\nPart 2: {pt2}")