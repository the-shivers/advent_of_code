import regex

with open('C:/Users/Brian/advent_of_code_2023/day1/input.txt', 'r') as file:
    lines = [line.strip() for line in file]
    
num_list = [str(i) for i in range(1,10)]
word_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
lookup = dict(zip(word_list + num_list, num_list + num_list))

pt1_pattern = '[0-9]'
pt2_pattern = '[0-9]|' + '|'.join(word_list)

def get_calibrations(lines, pattern):
    calibration_list = []
    for i in lines:
        matches = regex.findall(pattern, i, overlapped=True)
        calibration_list += [
            int(lookup[matches[0]] + lookup[matches[-1]])
        ]
    return calibration_list

print('Part 1 solution:', sum(get_calibrations(lines, pt1_pattern)))
print('Part 2 solution:', sum(get_calibrations(lines, pt2_pattern)))

####################### ATTEMPT 2 #######################

def calibrate_string(s, check_list):
    first = False
    last = False
    for i in range(len(s)):
        for check in check_list:
            if not first and check in s[0:i+1]:
                first = 10 * int(lookup[check])
            if not last and check in s[-i-1:]:
                last = int(lookup[check])
        if first and last:
            break
    return first + last
        
print('Part 1 solution:', sum([calibrate_string(i, num_list) for i in lines]))
print('Part 2 solution:', sum([calibrate_string(i, num_list+word_list) for i in lines]))

####################### ATTEMPT 3 #######################

import re

stupid_words = ['o1e', 't2o', 't3e', '4', '5e', '6', '7n', 'e8t', 'n9e']
stupid_dict = dict(zip(word_list, stupid_words))

def clean_string(s, words=False):
    if words:
        for key, value in stupid_dict.items():
            s = s.replace(key, value)
    s = re.sub("[^0-9]", "", s)
    return int(s[0] + s[-1])

print('Part 1 solution:', sum([clean_string(i) for i in lines]))
print('Part 2 solution:', sum([clean_string(i, True) for i in lines]))

####################### MASHI #######################

from typing import Dict, List

pt1_pattern_m = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}

pt2_pattern_m = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}
    
def is_digit(s: str, i: int, pattern: Dict[str, str]):
    for key in pattern:
        if i + len(key) > len(s):
            continue
        else:
            if s[i:i+len(key)] == key:
                return pattern[key]
    return False

def get_digits(s: str, pattern: Dict[str, str]):
    first = ""
    last = ""
    for i in range(len(s)):
        d = is_digit(s, i, pattern)
        if d != False:
            first = d
            break
    for i in range(len(s) - 1, -1, -1):
        d = is_digit(s, i, pattern)
        if d != False:
            last = d
            break
    return int(first + last)

def get_calibrations_m(lines: List[str], pattern: Dict[str, str]):
    calibrations: List[int] = []
    for line in lines:
        calibrations.append(get_digits(line, pattern))
    return calibrations

####################### TIMING #######################

import time

# https://0x0.st/HxMf.txt
with open('C:/Users/Brian/advent_of_code_2023/day1/bigboy.txt', 'r') as file:
    big_lines = [line.strip() for line in file]
    
solutions = [
    (lambda: sum(get_calibrations(big_lines, pt1_pattern)), "Solution 1 pt 1"),
    (lambda: sum(get_calibrations(big_lines, pt2_pattern)), "Solution 1 pt 2"),
    (lambda: sum([calibrate_string(i, num_list) for i in big_lines]), "Solution 2 pt 1"),
    (lambda: sum([calibrate_string(i, num_list+word_list) for i in big_lines]), "Solution 2 pt 2"),
    (lambda: sum([clean_string(i) for i in big_lines]), "Solution 3 pt 1"),
    (lambda: sum([clean_string(i, True) for i in big_lines]), "Solution 3 pt 2"),
    (lambda: sum(get_calibrations_m(big_lines, pt1_pattern_m)), "Mashi solution pt 1"),
    (lambda: sum(get_calibrations_m(big_lines, pt2_pattern_m)), "Mashi solution pt 2")
]

for solution, description in solutions:
    start_time = time.time()
    result = solution()  # Execute the function
    end_time = time.time()
    print(description + " - Execution time:", end_time - start_time, "seconds")

# Solution 1 pt 1 - Execution time: 3.6426374912261963 seconds
# Solution 1 pt 2 - Execution time: 5.685629844665527 seconds
# Solution 2 pt 1 - Execution time: 9.558983564376831 seconds
# Solution 2 pt 2 - Execution time: 8.025240898132324 seconds
# Solution 3 pt 1 - Execution time: 1.733159065246582 seconds
# Solution 3 pt 2 - Execution time: 2.4082448482513428 seconds
# Mashi solution pt 1 - Execution time: 16.141472101211548 seconds
# Mashi solution pt 2 - Execution time: 10.743357181549072 seconds
