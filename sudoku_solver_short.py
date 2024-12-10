board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

f = 0 # iteration counter

def findEmpties(board):
    out = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                out.append((i, j))
    return out

def isValid(board, pos, num):
    row = pos[0]
    col = pos[1]

    if board[row][col] == 0:
        return True
    # check rows
    for index, i in enumerate(board[row]):
        if i == num and index != col: # if there's the same number as the input "num" that's not at "pos", it's a violation
            return False

    # check columns
    for i in range(len(board)):
        if board[i][col] == num and i !=  row: # same but for columns
            return False

    # check box
    boxX = col // 3 # assigns number to box [0-2][0-2]
    boxY = row // 3

    for i in range(boxY*3, boxY*3+3):
        for j in range(boxX*3, boxX*3+3):
            if board[i][j] == num and (i, j) != (row, col):
                return False
    return True

def incAndCheck(board, empties, empty): # "empty" will need tuple
    emptyPos = empties.index(empty)
    cRow, cCol = empty
    global f
    while True:
        f += 1 # iterations counter
        if board[cRow][cCol] + 1 < 10:
            board[cRow][cCol] += 1
            if isValid(board, [cRow, cCol], board[cRow][cCol]):
                return True
        elif emptyPos == 0:
            return None
        else:
            board[cRow][cCol] = 0
            emptyPos -=1
            cRow, cCol = empties[emptyPos]
            
def solve(board):
    solutions = []  # List to store multiple solutions
    empties = findEmpties(board)

    def backtrack(empties_index):
        if empties_index == len(empties):
            solutions.append([row[:] for row in board])  # Store the current solution
            return
        row, col = empties[empties_index]
        for num in range(1, 10):
            if isValid(board, (row, col), num):
                board[row][col] = num
                backtrack(empties_index + 1)
                board[row][col] = 0  # Backtrack

    # Start backtracking from the first empty cell
    backtrack(0)

    return solutions

board = solve(board)
if board:
    print(f"\n{len(board)} solutions found")
    if len(board) > 3: # no more than 3 boards printed
        for i in range(3):
            print(f"\nSolution {i}:")
            print_board(board[i])
    else:
        for solution in board:
            print_board(solution)
else:
    print("\nNo solutions found")
