example = 'advent_of_code/2023/day7/example.txt'
input_txt = 'advent_of_code/2023/day7/input.txt'
with open(input_txt) as file:
    lines = [[line.strip().split()[0], int(line.strip().split()[1])]  for line in file]

cards = 'A K Q J T 9 8 7 6 5 4 3 2'.split()[::-1]

from collections import Counter

def classify_hand(hand_str):
    letter_counts = Counter(hand_str)
    max_occur = letter_counts.most_common(1)[0][1]
    if max_occur == 5:
        return 'five of a kind'
    elif max_occur == 4:
        return 'four of a kind'
    elif max_occur == 3 and len(set(hand_str)) == 2:
        return 'full house'
    elif max_occur == 3:
        return 'three of a kind'
    elif max_occur == 2 and len(set(hand_str)) == 3:
        return 'two pair'
    elif max_occur == 2:
        return 'one pair'
    else:
        return 'high card'
    
first_digit = {
    'five of a kind': 9,
    'four of a kind': 8,
    'full house': 7,
    'three of a kind': 6,
    'two pair': 5,
    'one pair': 4,
    'high card': 3
}
    
def get_sort_val(updated_line):
    val = 0
    val += updated_line[-1][-1] * (16 ** 0)
    val += updated_line[-1][-2] * (16 ** 1)
    val += updated_line[-1][-3] * (16 ** 3)
    val += updated_line[-1][-4] * (16 ** 4)
    val += updated_line[-1][-5] * (16 ** 5)
    val += first_digit[updated_line[2]] * (16 ** 6)
    return val

# for line in lines:
#     line.append(classify_hand(line[0]))
#     line.append([cards.index(line[0][i]) for i in range(5)])
#     line.append(get_sort_val(line))

# sorted_data = sorted(lines, key=lambda x: x[-1])

# for i, line in enumerate(sorted_data):
#     line.append(i + 1)

# sum([item[1] * item[-1] for item in sorted_data])

# Part 2
cards = 'A K Q T 9 8 7 6 5 4 3 2 J'.split()[::-1]

joker_count = sum(1 for i in 'T55J5' if i == 'J')
joker_first = 'T55J5'[0] == 'J'


def classify_hand_jokers(hand_str):
    joker_count = sum(1 for i in hand_str if i == 'J')
    if joker_count == 5:
        return 'five of a kind', 'AAAAA'
    joker_first = hand_str[0] == 'J'
    jokerless = hand_str.replace('J', '')
    letter_counts = Counter(jokerless)
    max_count = 0
    max_card = ''
    for card, count in letter_counts.items():
        # Check if the count is higher than the current maximum
        if count > max_count:
            max_count = count
            max_card = card
        # If counts are equal, compare the index in the cards list
        elif count == max_count and cards.index(card) > cards.index(max_card):
            max_card = card
    result_string = hand_str.replace('J', max_card)
    letter_counts2 = Counter(result_string)
    max_occur = letter_counts2.most_common(1)[0][1]
    if max_occur == 5:
        return 'five of a kind', result_string
    elif max_occur == 4:
        return 'four of a kind', result_string
    elif max_occur == 3 and len(set(result_string)) == 2:
        return 'full house', result_string
    elif max_occur == 3:
        return 'three of a kind', result_string
    elif max_occur == 2 and len(set(result_string)) == 3:
        return 'two pair', result_string
    elif max_occur == 2:
        return 'one pair', result_string
    else:
        return 'high card', result_string
    
new_lines = []
for line in lines:
    print(line)
    orig_hand = line[0][:]
    if 'J' in line[0]:
        classification, new_hand = classify_hand_jokers(line[0])
        line[0] = new_hand
        line.append(classification)
    else:
        line.append(classify_hand(line[0]))
    print(line)
    line.append([cards.index(orig_hand[i]) for i in range(5)])
    line.append(get_sort_val(line))
    line = [orig_hand] + line
    print(line)
    new_lines.append(line)
    
    
    
sorted_data = sorted(new_lines, key=lambda x: x[-1])
for i, line in enumerate(sorted_data):
    line.append(i + 1)
    
sum([item[2] * item[-1] for item in sorted_data]) # NOT 254494947
