import numpy as np

input_txt = 'input.txt'
with open(input_txt) as file:
    curr_game = 0
    games = []
    for line in file:
        if "Button A: " in line:
            games.append({})
            loc = line.strip().split('Button A: ')[1]
            x_str, y_str = loc.split(', ')
            games[curr_game]['A'] = {"X": int(x_str.split("X+")[1]), "Y": int(y_str.split("Y+")[1])}
        elif "Button B: " in line:
            loc = line.strip().split('Button B: ')[1]
            x_str, y_str = loc.split(', ')
            games[curr_game]['B'] = {"X": int(x_str.split("X+")[1]), "Y": int(y_str.split("Y+")[1])}
        elif "Prize: " in line:
            loc = line.strip().split('Prize: ')[1]
            x_str, y_str = loc.split(', ')
            games[curr_game]['P'] = {"X": int(x_str.split("X=")[1]), "Y": int(y_str.split("Y=")[1])}
            games[curr_game]['P2'] = {"X": 10000000000000 + int(x_str.split("X=")[1]), "Y": 10000000000000 + int(y_str.split("Y=")[1])}
            curr_game += 1

def solve_game(game):
    a_dict =  {}
    solutions = []
    curr_x, curr_y = 0, 0
    count = 0
    while curr_x < game['P']['X'] and curr_y < game['P']['Y']:
        a_dict[(curr_x, curr_y)] = count
        curr_x += game['A']['X']
        curr_y += game['A']['Y']
        count += 1
    curr_x, curr_y = 0, 0
    count = 0
    while curr_x < game['P']['X'] and curr_y < game['P']['Y']:
        target_x, target_y = game['P']['X'] - curr_x, game['P']['Y'] - curr_y
        if (target_x, target_y) in a_dict:
            solutions.append({'A': a_dict[(target_x, target_y)], 'B': count})
        curr_x += game['B']['X']
        curr_y += game['B']['Y']
        count += 1
    return solutions

def find_integer_coefficients(v1, v2, target):
    A = np.array([[v1[0], v2[0]], 
                  [v1[1], v2[1]]])
    b = np.array(target)
    try:
        solution = np.linalg.solve(A, b)
        a, b = solution[0], solution[1]
        if abs(a - round(a)) < 1e-2 and abs(b - round(b)) < 1e-2:
            a, b = int(round(a)), int(round(b))
            computed = (a * v1[0] + b * v2[0], a * v1[1] + b * v2[1])
            if computed == target:
                return a, b
        return None
    except:
        return None

pt1 = pt2 = 0
for game in games:
    solutions = solve_game(game)
    if solutions:
        pt1 += 3 * solutions[0]['A'] + 1 * solutions[0]['B']
    result = find_integer_coefficients((game['A']['X'], game['A']['Y']), (game['B']['X'], game['B']['Y']), (game['P2']['X'], game['P2']['Y']))
    if result:
        pt2 += 3 * result[0] + 1 * result[1]
print(pt1)
print(pt2)
    
