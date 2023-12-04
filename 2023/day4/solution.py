with open('advent_of_code_2023/day4/input.txt') as file:
    lines = [line.strip() for line in file]
    
# Example line: Card   1: 98 16 95 90 53 33 43  7 46 45 | 85 15 78 57 34 10 46 90 33 13  8 54  4 37 25 63 55 41  7 82 69 16 30 76  2
    
# Part 1
import re

def convert_string_to_lists(no_game_str):
    parts = no_game_str.split('|')
    list1 = [int(num) for num in parts[0].strip().split()]
    list2 = [int(num) for num in parts[1].strip().split()]
    return list1, list2
            
def get_points(raw_string):
    no_game = raw_string.split(': ')[1]
    list1, list2 = convert_string_to_lists(no_game)
    my_points = 0
    for my_num in list2:
        if my_num in list1:
            if my_points == 0:
                my_points = 1
            else:
                my_points *= 2
    return my_points

sum([get_points(line) for line in lines])

# Part 2
def count_wins(raw_string):
    no_game = raw_string.split(': ')[1]
    list1, list2 = convert_string_to_lists(no_game)
    my_wins = 0
    for my_num in list2:
        if my_num in list1:
            my_wins += 1
    return my_wins
    
copies_dict = dict(zip(range(1, len(lines) + 1), [1]*len(lines)))
wins_dict = dict(zip(range(1, len(lines) + 1), [0]*len(lines)))

for index, line in enumerate(lines):
    wins_dict[index+1] = count_wins(line)

for game, wins in wins_dict.items():
    for j in range(copies_dict[game]):
        for i in range(wins):
            copies_dict[game + 1 + i] += 1
        
sum(copies_dict.values())