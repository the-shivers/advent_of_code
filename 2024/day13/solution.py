def get_games(filename):
    with open(filename) as file:
        games = []
        for line in file:
            if "Button A: " in line:
                games.append({})
                loc = line.strip().split(': ')[1]
                games[-1]['A'] = tuple(map(int, [i[2:] for i in loc.split(', ')]))
            elif "Button B: " in line:
                loc = line.strip().split(': ')[1]
                games[-1]['B'] = tuple(map(int, [i[2:] for i in loc.split(', ')]))
            elif "Prize: " in line:
                loc = line.strip().split(': ')[1]
                games[-1]['P'] = tuple(map(int, [i[2:] for i in loc.split(', ')]))
                games[-1]['P2'] = tuple(i + 10**13 for i in games[-1]['P'])
    return games

def get_coefficients(v1, v2, target):
    """Cramer's rule. Checks if vals close to integer before returning. 
    Input never has a zero determinant, so we don't worry about it."""
    det = v1[0] * v2[1] - v1[1] * v2[0]
    a = (target[0] * v2[1] - target[1] * v2[0]) / det
    b = (v1[0] * target[1] - v1[1] * target[0]) / det
    if abs(a - round(a)) < 1e-10 and abs(b - round(b)) < 1e-10:
        return round(a), round(b)
    return None

def solve(filename):
    games = get_games(filename)
    pt1 = pt2 = 0
    for game in games:
        result1 = get_coefficients(game['A'], game['B'], game['P'])
        if result1:
            pt1 += 3 * result1[0] + 1 * result1[1]
        result2 = get_coefficients(game['A'], game['B'], game['P2'])
        if result2:
            pt2 += 3 * result2[0] + 1 * result2[1]
    print(f"Part 1: {pt1}\nPart 2: {pt2}")
          
if __name__ == "__main__":
    solve('input.txt')



    
