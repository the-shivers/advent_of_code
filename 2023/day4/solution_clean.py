with open('advent_of_code_2023/day4/input.txt') as file:
    games = [line.strip() for line in file]

def get_number_lists(game):
    winners_str, numbers_str = game.split(': ')[1].split(' | ')
    winners = [int(i) for i in winners_str.split()]
    numbers = [int(i) for i in numbers_str.split()]
    return winners, numbers

def get_points(game, is_pt_2 = False):
    winners, numbers = get_number_lists(game)
    match_count  = sum(num in winners for num in numbers)
    if is_pt_2:
        return match_count
    return 2 ** (match_count - 1) if match_count > 0 else 0

def get_copies_list(games):
    copies = [1] * len(games)
    for index, game in enumerate(games):
        wins = get_points(game, True)
        for i in range(copies[index]):
            for j in range(wins):
                copies[index + 1 + j] += 1
    return copies

print("Part 1:", sum([get_points(game) for game in games])) # 26426
print("Part 2:", sum(get_copies_list(games))) # 6227972