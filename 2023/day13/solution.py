


def get_puzzles(filename):
    puzzles = [[]]
    with open(filename) as lines:
        for line in lines:
            stripped = line.strip()
            if len(stripped) == 0:
                puzzles.append([])
            else:
                puzzles[-1].append(stripped)
    return puzzles

def get_horizontal_sym_line(puzzle):
    rows = len(puzzle)
    for sym_line in range(rows - 1):
        ind1, ind2 = sym_line, sym_line + 1
        while puzzle[ind1] == puzzle[ind2]:
            if ind1 - 1 in range(rows) and ind2 + 1 in range(rows):
                ind1 -= 1
                ind2 += 1
            else:
                return(sym_line, sym_line + 1)
    return None


def get_vertical_sym_line(puzzle):
    cols = len(puzzle[0])
    for sym_line in range(cols - 1):
        ind1, ind2 = sym_line, sym_line + 1
        while [line[ind1] for line in puzzle] == [line[ind2] for line in puzzle]:
            if ind1 - 1 in range(cols) and ind2 + 1 in range(cols):
                ind1 -= 1
                ind2 += 1
            else:
                return(sym_line, sym_line + 1)
    return None

def score_puzzle(puzzle):
    horiz_result = get_horizontal_sym_line(puzzle)
    vert_result = get_vertical_sym_line(puzzle)
    if horiz_result and vert_result:
        raise ValueError('You found too many results!')
    elif horiz_result:
        return horiz_result[1] * 100
    elif vert_result:
        return vert_result[1]
    else:
        raise ValueError('You found too few results!')

def solve_pt_1(puzzles):
    result = 0
    for puzzle in puzzles:
        result += score_puzzle(puzzle)
    return result # 25519 (too low)


filename = 'input.txt'
filename = 'example.txt'
filename = 'example2.txt'
puzzles = get_puzzles(filename)


solve_pt_1(puzzles) # 27202


# If we take the difference of items in comparison rows and only one row is off by one, we've found our smudge

def get_horizontal_sym_line2(puzzle):
    rows = len(puzzle)
    for sym_line in range(rows - 1):
        # get sum of all parts before line, compare to sum of all parts after line
        pre_sum = []
        ind1, ind2 = sym_line, sym_line + 1
        while puzzle[ind1] == puzzle[ind2]:
            if ind1 - 1 in range(rows) and ind2 + 1 in range(rows):
                ind1 -= 1
                ind2 += 1
            else:
                return(sym_line, sym_line + 1)
    return None


# score_puzzle(puzzles[0])




# 41566

# import numpy as np

# def mirrorpos(arr, axis=0, diff=0):
#     m = np.array(arr, dtype=int)
#     if axis == 1:
#         m = m.T
#     for i in range(m.shape[0] - 1):
#         upper_flipped = np.flip(m[: i + 1], axis=0)
#         lower = m[i + 1 :]
#         rows = min(upper_flipped.shape[0], lower.shape[0])
#         if np.count_nonzero(upper_flipped[:rows] - lower[:rows]) == diff:
#             return i + 1
#     return 0

# with open("input.txt", "r") as file:
#     data = file.read().split("\n\n")
# for i in range(2):
#     total = 0
#     for puzzle in data:
#         arr = []
#         for line in puzzle.splitlines():
#             arr.append([*line.strip().replace(".", "0").replace("#", "1")])
#         total += 100 * mirrorpos(arr, axis=0, diff=i) + mirrorpos(arr, axis=1, diff=i)
#     print(total)


# filename = 'input.txt'
# puzzles = get_puzzles(filename)


# mysum, hissum = 0, 0
# for i, puzzle in enumerate(puzzles):
#     mine = score_puzzle(puzzle)
#     arr = []
#     for line in puzzle:
#         arr.append([*line.strip().replace(".", "0").replace("#", "1")])
#     correct = 100 * mirrorpos(arr, axis=0, diff=0) + mirrorpos(arr, axis=1, diff=0)
#     if correct != mine:
#         print(i, mine, correct)
#     mysum += mine
#     hissum += correct