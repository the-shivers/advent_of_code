with open('advent_of_code/2023/day7/input.txt') as file:
    lines = [{'hand': line.split()[0], 'bet': int(line.split()[1])} 
             for line in file]

cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
hand_classification = {
    'five of a kind': 7,
    'four of a kind': 6,
    'full house': 5,
    'three of a kind': 4,
    'two pair': 3,
    'one pair': 2,
    'high card': 1
}

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
    
def get_sort_val(classification, hand_str):
    val = 0
    for i, card in enumerate(hand_str[::-1]):
        val += cards.index(card) * (16 ** i)
    val += hand_classification[classification] * (16 ** (i + 1))
    return val
    
def dejoker(hand_str):
    joker_count = sum(1 for i in hand_str if i == 'J')
    if joker_count == 5:
        return 'AAAAA'
    jokerless = hand_str.replace('J', '')
    letter_counts = Counter(jokerless)
    max_count = 0
    max_card = ''
    for card, count in letter_counts.items():
        if count > max_count:
            max_count = count
            max_card = card
        elif count == max_count and cards.index(card) > cards.index(max_card):
            max_card = card
    return hand_str.replace('J', max_card)
    
# Part 1
pt1_hands = []
for hand in lines:
    classification = classify_hand(hand['hand'])
    sort_val = get_sort_val(classification, hand['hand'])
    pt1_hands.append(hand | {'class': classification, 'sort_val': sort_val})
pt1_hands_sorted = sorted(pt1_hands, key=lambda x: x['sort_val'])
for i, d in enumerate(pt1_hands_sorted):
    d['rank'] = i + 1

sum([hand['bet'] * hand['rank'] for hand in pt1_hands_sorted]) # 253866470

# Part 2
cards = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
pt2_hands = []
for hand in lines:
    classification = classify_hand(dejoker(hand['hand']))
    sort_val = get_sort_val(classification, hand['hand'])
    pt2_hands.append(hand | {'class': classification, 'sort_val': sort_val})
pt2_hands_sorted = sorted(pt2_hands, key=lambda x: x['sort_val'])
for i, d in enumerate(pt2_hands_sorted):
    d['rank'] = i + 1
    
sum([hand['bet'] * hand['rank'] for hand in pt2_hands_sorted]) # 254494947
    
