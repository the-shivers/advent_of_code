input_txt = 'advent_of_code/2023/day6/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]
    
# Part 1
times = [int(t) for t in lines[0].split()[1:]]
distances = [int(d) for d in lines[1].split()[1:]]

ways = 1
for t, d in zip(times, distances):
    curr_race_ways = 0 
    for ms in range(t + 1):
        curr_race_ways += 1 if (t - ms) * ms > d else 0
    ways *= curr_race_ways

print("Part 1:", ways) # 5133600

# Part 2
time = int("".join(lines[0].split()[1:]))
distance = int("".join(lines[1].split()[1:]))

ways = 0
for ms in range(time + 1):
    ways += 1 if (time - ms) * ms > distance else 0

print("Part 2:", ways) # 40651271, in about 6 seconds