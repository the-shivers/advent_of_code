from math import prod

def get_max_dict(game):
    turn_dicts = []
    for turn_str in game.split(': ')[1].split('; '):
        turn_dict = {}
        for qty_color_str in turn_str.split(', '):
            qty, color = qty_color_str.split()
            turn_dict[color[0]] = int(qty)
        turn_dicts.append({'r': 0, 'g': 0, 'b': 0} | turn_dict)
    return {c: max(t[c] for t in turn_dicts) for c in ['r', 'g', 'b']}

def analyze_game(game, target):
    max_dict = get_max_dict(game)
    return {
        'is_possible': all(max_dict[k] <= target[k] for k in max_dict),
        'product': prod(max_dict.values())
    }

def get_solutions(game_list, target):
    possible_ids = []
    product_list = []
    for counter, game in enumerate(game_list):
        info = analyze_game(game, target)
        if info['is_possible']:
            possible_ids.append(counter + 1)
        product_list.append(info['product'])
    print('Part 1:', sum(possible_ids))
    print('Part 2:', sum(product_list))
    
with open('advent_of_code_2023/day2/input.txt') as file:
    games = file.read().strip().split('\n')
    
target = {'r': 12, 'g': 13, 'b': 14}
get_solutions(games, target)