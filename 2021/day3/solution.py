# Part 1 Stuff
def get_digit_counts(lines):
    digit_counts = {i: {'0': 0, '1': 0} for i in range(len(lines[0]))}
    for line in lines:
        for i, digit in enumerate(line):
            digit_counts[i][digit] += 1
    return digit_counts

def get_most_and_least_common_digits(lines, digit_counts):
    most_common = [0] * len(lines[0])
    least_common = [0] * len(lines[0])
    for key, value in digit_counts.items():
        if value['0'] == value['1']:
            raise ValueError('That was not supposed to happen.')
        elif value['0'] > value['1']:
            most_common[key] = 0 # pointless but oh well
            least_common[key] = 1
        else:
            most_common[key] = 1
            least_common[key] = 0 # pointless but oh well
    return most_common, least_common

def digit_list_to_num(digit_list):
    return int(''.join([str(i) for i in digit_list]), 2)

def part1(lines):
    digit_counts = get_digit_counts(lines)
    most_common, least_common = get_most_and_least_common_digits(lines, digit_counts)
    result = digit_list_to_num(most_common) * digit_list_to_num(least_common)
    return result


# Part 2 stuff
def filter(remaining_lines, i, type = 'oxygen'):
    counter = {'0': 0, '1': 0}
    result = []
    for line in remaining_lines:
        counter[line[i]] += 1
    if type == 'oxygen':
        if counter['1'] >= counter['0']:
            key = '1'
        else:
            key = '0'
    else:
        if counter['1'] >= counter['0']:
            key = '0'
        else:
            key = '1'
    for line in remaining_lines:
        if line[i] == key:
            result.append(line)
    return result if result else remaining_lines[-1]

def get_rating(lines, type):
    for i in range(len(lines[0])):
        lines = filter(lines, i, type)
        if len(lines) == 1:
            break
    return lines
    
def part2(lines):
    oxygen = get_rating(lines, 'oxygen')[0]
    co2 = get_rating(lines, 'co2')[0]
    return int(oxygen, 2) * int(co2, 2)


if __name__ == '__main__':
    with open('input.txt') as raw_lines:
        lines = [line.strip() for line in raw_lines]
    print(f'Pt 1 result is: {part1(lines)}')
    print(f'Pt 2 result is: {part2(lines)}')
    

    
