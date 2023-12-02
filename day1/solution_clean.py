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

####################### RACE #######################

import time

with open('C:/Users/Brian/advent_of_code_2023/day1/bigboy.txt', 'r') as file:
    lines = [line.strip() for line in file]

start_time = time.time()
sum(get_calibrations(lines, pt1_pattern))
end_time = time.time()
print("Solution 1, Pt 1:", end_time - start_time)

start_time = time.time()
sum(get_calibrations(lines, pt2_pattern))
end_time = time.time()
print("Solution 1, Pt 2:", end_time - start_time)

start_time = time.time()
sum([calibrate_string(i, num_list) for i in lines])
end_time = time.time()
print("Solution 2, Pt 1:", end_time - start_time)

start_time = time.time()
sum([calibrate_string(i, num_list+word_list) for i in lines])
end_time = time.time()
print("Solution 2, Pt 2:", end_time - start_time)

start_time = time.time()
sum([clean_string(i) for i in lines])
end_time = time.time()
print("Solution 3, Pt 1:", end_time - start_time)

start_time = time.time()
sum([clean_string(i, True) for i in lines])
end_time = time.time()
print("Solution 3, Pt 2:", end_time - start_time)

# Solution 1, Pt 1: 3.7184317111968994
# Solution 1, Pt 2: 5.692614555358887

# Solution 2, Pt 1: 9.227832555770874
# Solution 2, Pt 2: 7.893181562423706

# Solution 3, Pt 1: 6.227064847946167
# Solution 3, Pt 2: 5.952021598815918
