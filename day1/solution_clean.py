import regex as re

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
        matches = re.findall(pattern, i, overlapped=True)
        calibration_list += [
            int(lookup[matches[0]] + lookup[matches[-1]])
        ]
    return calibration_list

print('Part 1 solution:', sum(get_calibrations(lines, pt1_pattern)))
print('Part 2 solution:', sum(get_calibrations(lines, pt2_pattern)))
