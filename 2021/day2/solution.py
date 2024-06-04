with open('input.txt') as lines:
    commands = [line.strip().split() for line in lines]

def pt1_solution(commands):
    horiz = 0
    depth = 0
    for command, amt in commands:
        if command == 'forward':
            horiz += int(amt)
        elif command == 'down':
            depth += int(amt)
        elif command == 'up':
            depth -= int(amt)
    return depth * horiz

def pt2_solution(commands):
    horiz, depth, aim = 0, 0, 0
    for command, amt in commands:
        if command == 'forward':
            horiz += int(amt)
            depth += aim * int(amt)
        elif command == 'down':
            aim += int(amt)
        elif command == 'up':
            aim -= int(amt)
    return depth * horiz


if __name__ == '__main__':
    print(f'Part 1 solution: {pt1_solution(commands)}')
    print(f'Part 2 solution: {pt2_solution(commands)}')