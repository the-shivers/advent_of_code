import time, sys
from functools import lru_cache

sys.setrecursionlimit(10**8)

def load_stones(filename='input.txt'):
    with open(filename) as file:
        return [int(i) for i in file.readline().split()]

def create_top_down_solution(multiplier):

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
            return quick_blink(stone * multiplier, num_blinks - 1)
    
    def solve(stones, num_blinks):
        return sum(quick_blink(stone, num_blinks) for stone in stones)
    
    return solve, quick_blink

def retarded_bottom_up_solution(stones, num_blinks, multiplier):
    
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
                get_distinct_stone_values(stone * multiplier, cache)

    cache = {}
    for stone in stones:
        get_distinct_stone_values(stone, cache)

    for stone in cache:
        cache[stone][0] = 1

    for blink in range(1, num_blinks + 1):
        for stone in cache:
            if stone == 0:
                cache[stone][blink] = cache[1][blink - 1]
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                half = len(s) // 2
                l, r = int(s[:half]), int(s[half:])
                cache[stone][blink] = cache[l][blink - 1] + cache[r][blink - 1]
            else:
                cache[stone][blink] = cache[stone * multiplier][blink - 1]

    return sum(cache[stone][num_blinks] for stone in stones)

def benchmark(blinks_list, multipliers):
    stones = load_stones()
    
    print(f"{'Multiplier':<10} {'Blinks':<10} {'Top-down (s)':<15} {'Bottom-up (s)':<15} {'Result':<20}")
    print("-" * 70)
    
    for multiplier in multipliers:
        print(multiplier)
        # Create a new top-down solution for this multiplier
        top_down_solve, quick_blink = create_top_down_solution(multiplier)
        
        for num_blinks in blinks_list:
            print(num_blinks)
            # Top-down timing
            start = time.time()
            top_result = top_down_solve(stones, num_blinks)
            top_time = time.time() - start
            
            # Bottom-up timing
            start = time.time()
            bottom_result = retarded_bottom_up_solution(stones, num_blinks, multiplier)
            bottom_time = time.time() - start
            
            # Verify results match
            assert top_result == bottom_result, f"Results don't match for {num_blinks} blinks with multiplier {multiplier}!"
            
            print(f"{multiplier:<10} {num_blinks:<10} {top_time:,.3f}         {bottom_time:,.3f}         {top_result:.2e}")
        
        # Clear the cache after we're done with this multiplier
        quick_blink.cache_clear()
        print("-" * 70)  # Separator between multipliers

if __name__ == "__main__":
    blinks_to_test = [75, 250, 1000]
    multipliers_to_test = [2024, 2616]
    benchmark(blinks_to_test, multipliers_to_test)