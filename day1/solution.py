# Read in inputs
file_loc = 'advent_of_code_2023/day1/input.txt'
with open(file_loc, 'r') as file:
    lines = [line.strip() for line in file]
    
example = [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet'
]

# Key funcs
def find_first_num(string):
    for char in string:
        if char.isnumeric():
            return char
        
def find_last_num(string):
    for char in string[::-1]:
        if char.isnumeric():
            return char
        
def get_calibration_list(str_list):
    return_list = []
    for i in str_list:
        return_list += [int(str(find_first_num(i) + find_last_num(i)))]
    return return_list

# return_list = get_calibration_list(example)
return_list = get_calibration_list(lines)
sum(return_list)

##### part two!
example2 = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen'
]

word_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
num_list = [str(i) for i in range(1,10)]
my_dict = dict(zip(word_list, num_list))

def find_first(string):
    for i in range(len(string)+1):
        substr = string[0:i]
        for j in word_list + num_list:
            if substr.find(j) > -1:
                if len(j) == 1:
                    return j
                else:
                    return my_dict[j]
        
def find_last(string):
    for i in range(len(string)+1):
        substr = string[-(i+1):]
        for j in word_list + num_list:
            if substr.find(j) > -1:
                if len(j) == 1:
                    return j
                else:
                    return my_dict[j]
                
def get_calibration_list2(str_list):
    return_list = []
    for i in str_list:
        return_list += [int(find_first(i) + find_last(i))]
    return return_list

# return_list = get_calibration_list2(example2)
return_list = get_calibration_list2(lines)

