example = 'advent_of_code/2023/day6/example.txt'
input_txt = 'advent_of_code/2023/day6/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]

times = lines[0].split()[1:]
distances = lines[1].split()[1:]
races = [{'t':int(times[i]), 'd':int(distances[i]), 'n':0} for i in range(len(times))]

# speed is time button is held down
def get_distance(hold_down_ms, total_ms):
    return (total_ms-hold_down_ms) * hold_down_ms

for r in races:
    for h in range(0, r['t'] + 1):
        if get_distance(h, r['t']) > r['d']:
            r['n'] += 1

from math import prod
ways = [i['n'] for i in races]
prod(ways)

# Part 2
sample_time = 71530
sample_dist = 940200
final_time = 53897698
final_dist = 313109012141201

# counter = 0
# for h in range(0, sample_time + 1):
#     if get_distance(h, sample_time) > sample_dist:
#         counter += 1

counter = 0
for h in range(0, final_time + 1):
    if h % 10000 == 0:
        print('at', h)
    if get_distance(h, final_time) > final_dist:
        counter += 1