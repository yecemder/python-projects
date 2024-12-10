# code idea:
# visit the board's empty (non-fixed) numbers (store them?) in some order
# start by placing a "1" in the first non-empty cell and check for violations
# if there are no violations (check constraints - row, column, box), advance to the next spot and fill in a 1
# if there are violations, advance the current number to 2
# keep incrementing until there are no violations
# if all 9 digits can't be in the spot, leave the spot blank, backtrack one spot and increment

# copy this into "board" to start a fresh new board

from timeit import default_timer as time

blankBoard = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

board = [
    [0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 9, 3, 8, 7, 0, 0],
    [9, 0, 0, 5, 0, 0, 0, 0, 6],
    [3, 0, 0, 4, 0, 5, 1, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 5, 2, 0, 9, 0, 0, 8],
    [1, 0, 0, 0, 0, 7, 0, 0, 2],
    [0, 0, 3, 8, 5, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 6, 0]
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

def backtrack(board, empties, empty): # "empty" will need tuple
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
    empties = findEmpties(board)
    # check to see if starting position is valid
    for i in range(9):
        for j in range(9):
            if not isValid(board, (i, j), board[i][j]):
                return None
    if len(empties) == 0:
        return True
    while True:
        cRow = None
        cCol = None
        for i, j in empties:
            if board[i][j] == 0:
                cRow = i
                cCol = j
                break
            
        if cRow is None and cCol is None:
            return board
        
        if backtrack(board, empties, (cRow, cCol)) is None:
            break
    return None

def print_board(board):
    if board is None:
        print("\nNo solution exists")
        return
    if not board:
        print("\nMultiple unique solutions exist")
        return
    if board is True:
        print("Board is already fully solved")
        return
    print("\nUnique solution:\n")
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

starttime = time()
board = solve(board)
timetaken = time() - starttime

print_board(board)
if board is True:
    pass

elif not board:
    print(f"\n{f} iterations to determine that this board has multiple unique solutions")

elif board is not None:
    print(f"\n{f} iterations to solve this board")

elif f != 0:
    print(f"\n{f} iterations to determine this board has no solutions")

else:
    print("starting position is invalid to solve")

print(f"took {timetaken} seconds to finish")
        
