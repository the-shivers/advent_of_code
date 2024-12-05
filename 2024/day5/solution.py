with open('advent_of_code/2024/day5/input.txt') as file:
    rules, updates = file.read().split('\n\n')
rules = [list(map(int, r.split('|'))) for r in rules.split('\n')]
updates = [list(map(int, u.split(','))) for u in updates.split('\n')]

def order_pages(update: list[int], rules: list[list[int]]) -> list[int]:
    """
    Since relevant rules always give a comparison of every page to every other
    page, we can just count unique pages coming before a given page--this will
    be the index in the correctly sorted list!
    """
    relevant_rules = {}
    sorted_nums = [0] * len(update)
    for src, dst in rules:
        if src in update and dst in update:
            if dst not in relevant_rules:
                relevant_rules[dst] = 0
            relevant_rules[dst] += 1
    for page in update:
        sorted_nums[relevant_rules.get(page, 0)] = page
    return sorted_nums

pt1, pt2 = 0, 0
for update in updates:
    sorted_update = order_pages(update, rules)
    if update == sorted_update:
        pt1 += update[len(update) // 2]
    else:
        pt2 += sorted_update[len(sorted_update) // 2]

print("Part 1:", pt1)
print("Part 2:", pt2)