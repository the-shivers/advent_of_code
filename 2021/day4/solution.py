def get_calls_and_boards(filename):
    with open(filename) as input:
        calls = [int(i) for i in input.readline().strip().split(',')]
        boards = []
        for line in input:
            if len(line.strip()) == 0:
                boards.append([])
            else:
                boards[-1].append([[int(i), False] for i in line.strip().split()])
    return calls, boards

def get_unmarked_nums(board):
    unmarked_numbers = []
    for row in board:
        for nums in row:
            if not nums[1]:
                unmarked_numbers.append(nums[0])
    return unmarked_numbers

def evaluate_rows(board):
    for row in board:
        row_status = True
        for nums in row:
            if not nums[1]:
                row_status = False
        if row_status:
            return True
    return False

def evaluate_cols(board):
    for col in range(len(board[0])):
        col_status = True
        for row in board:
            if not row[col][1]:
                col_status = False
        if col_status:
            return True
    return False

def pt1_bingo_game(calls, boards):
    for call in calls:
        for b, board in enumerate(boards):
            for r, row in enumerate(board):
                for c, num in enumerate(row):
                    if num[0] == call:
                        num[1] = True
                        # print(f'Board {b} got {call} in row {r} and col {c}!')
            if evaluate_rows(board) or evaluate_cols(board):
                return sum(get_unmarked_nums(board)) * call
            
def pt2_bingo_game(calls, boards):
    victory_list = [False] * len(boards)
    loser_index = -1
    for call in calls:
        for b, board in enumerate(boards):
            for r, row in enumerate(board):
                for c, num in enumerate(row):
                    if num[0] == call:
                        num[1] = True
                        # print(f'Board {b} got {call} in row {r} and col {c}!')
            if evaluate_rows(board) or evaluate_cols(board):
                victory_list[b] = True
            if sum(victory_list) + 1 == len(victory_list):
                loser_index = victory_list.index(False)
            if loser_index > -1 and b == loser_index and (evaluate_rows(board) or evaluate_cols(board)):
                return sum(get_unmarked_nums(boards[b])) * call

            
if __name__ == '__main__':
    filename = 'input.txt'
    calls, boards = get_calls_and_boards(filename)
    print(f'Part 1 answer: {pt1_bingo_game(calls, boards)}')
    print(f'Part 2 answer: {pt2_bingo_game(calls, boards)}')