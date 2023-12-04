file_loc = 'advent_of_code_2023/day2/input.txt'
with open(file_loc, 'r') as file:
    lines = [line.strip() for line in file]
    
import re
    
target = {'red': 12, 'green': 13, 'blue': 14, 'ttl': 12 + 13 + 14}
colors = ['red', 'green', 'blue']

def get_pull_dict(pull_str):
    pull_dict = {'red': 0, 'green': 0, 'blue': 0, 'ttl': 0}
    color_strs = pull_str.split(', ')
    for i in color_strs:
        for color in colors:
            if color in i:
                pull_dict[color] += int(re.sub("[^0-9]", "", i))
                pull_dict['ttl'] += int(re.sub("[^0-9]", "", i))
    return pull_dict

def get_max_dict(game):
    max_dict = {'red': 0, 'green': 0, 'blue': 0, 'ttl': 0}
    pulls = re.sub(r"Game \d+: ", "", game).split(';')
    pull_dicts = [get_pull_dict(i) for i in pulls]
    for pull_dict in pull_dicts:
        for key, value in pull_dict.items():
            if value >= max_dict[key]:
                max_dict[key] = value
    return max_dict

def get_valid_games(game_list):
    valid_games = []
    for counter, i in enumerate(game_list):
        valid = True
        max_dict = get_max_dict(i)
        for key, value in max_dict.items():
            if value > target[key]:
                valid = False
        if valid:
            valid_games += [counter+1]
    return valid_games

def get_powers(game_list):
    power_list = []
    for counter, i in enumerate(game_list):
        max_dict = get_max_dict(i)
        cur = 1
        for key, value in max_dict.items():
            if key != 'ttl':
                cur = cur * value
        power_list += [cur]
    return power_list

sum(get_valid_games(lines)) # 2278
sum(get_powers(lines)) # 67953



