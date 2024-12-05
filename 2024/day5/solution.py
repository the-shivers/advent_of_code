# input_txt = 'advent_of_code/2024/day5/example.txt'
input_txt = 'advent_of_code/2024/day5/input.txt'
rules = []
updates = []
with open(input_txt) as file:
    for line in file:
        if '|' in line.strip():
            rule = [int(i) for i in line.strip().split('|')]
            rules.append(rule)
        elif ',' in line.strip():
            update = [int(i) for i in line.strip().split(',')]
            updates.append(update)

def get_middle_page_number(update: list[int]) -> int:
    return update[len(update) // 2]

def test_update(update: list[int], rules: list[list[int]]) -> bool:
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) > update.index(rule[1]):
                return False
        else:
            continue
    return True

# Part 1
total = 0
for update in updates:
    if test_update(update, rules):
        total += get_middle_page_number(update)
print(total)

# Part 2
def get_loss_dict(rules: list[list[int]]) -> dict[int, int]:
    dict = {}
    for rule in rules:
        if rule[0] in dict:
            dict[rule[0]] += 1
        else:
            dict[rule[0]] = 1
    return dict

def order_update(update: list[int], rules: list[list[int]]) -> list[int]:
    relevant_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            relevant_rules.append(rule)
    ordered = [0] * len(update)
    loss_dict = get_loss_dict(relevant_rules)
    sorted_keys = sorted(loss_dict.keys(), key=loss_dict.get, reverse=True)
    for page in update:
        if page in sorted_keys:
            ordered[sorted_keys.index(page)] = page
        else:
            ordered[-1] = page
    return ordered

total = 0
for update in updates:
    if not test_update(update, rules):
        ordered = order_update(update, rules)
        total += get_middle_page_number(ordered)
print(total)