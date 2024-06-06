def get_fish(filename):
    with open(filename) as raw_input:
        return [int(i) for i in raw_input.readline().strip().split(',')]
    
def get_fish_dict(fish):
    fish_dict = {i:0 for i in range(9)}
    for f in fish:
        fish_dict[f] += 1
    return fish_dict

def simulate_day(i, fish):
    result = []
    new_fish = 0
    for f in fish:
        if f == 0:
            result.append(6)
            new_fish += 1
        else:
            result.append(f - 1)
    result += [8] * new_fish
    # print(f'Result for day {i}: {len(result)}')
    return result

def simulation(days, fish):
    for i in range(days):
        fish = simulate_day(i, fish)
    return len(fish)

# Performance Improvements for Part 2
def simulate_dict_day(day, fish_dict):
    new_fish_dict = {}
    for i in range(8):
        new_fish_dict[i] = fish_dict[i + 1]
    new_fish_dict[8] = fish_dict[0]
    new_fish_dict[6] += fish_dict[0]
    # print(f'Result for day {day}: {sum(new_fish_dict.values())}')
    return new_fish_dict

def simulation_dict(days, fish_dict):
    for i in range(days):
        fish_dict = simulate_dict_day(i, fish_dict)
    return sum(fish_dict.values())
    



if __name__ == '__main__':
    filename = 'input.txt'
    fish = get_fish(filename)
    print(f'Part 1 result: {simulation(80, fish)}')

    fish_dict = get_fish_dict(fish)
    print(f'Part 2 result: {simulation_dict(256, fish_dict)}')
