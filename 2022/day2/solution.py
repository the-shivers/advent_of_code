with open('advent_of_code/2022/day2/input.txt') as file:
    lines = [line.strip() for line in file]
    
e = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
p = {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}
s = {'rock': 1, 'paper': 2, 'scissors': 3}

def score_round(line):
    elf, you = line.split()
    score = s[p[you]]
    score += 6 if p[you] == 'rock' and e[elf] == 'scissors' else 0
    score += 6 if p[you] == 'scissors' and e[elf] == 'paper' else 0
    score += 6 if p[you] == 'paper' and e[elf] == 'rock' else 0
    score += 3 if p[you] == e[elf] else 0
    return score

print('Pt 1:', sum([score_round(line) for line in lines])) # 11063

# pt 2
g = {'X': 0, 'Y': 3, 'Z': 6}
listy = ['scissors', 'rock', 'paper']
def score_round(line):
    elf, score = line.split()
    return g[score] + s[listy[(listy.index(e[elf]) + g[score] // 3 - 1) % 3]]

print('Pt 2:', sum([score_round(line) for line in lines])) # 10349