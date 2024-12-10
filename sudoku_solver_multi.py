# code idea:
# visit the board's empty (non-fixed) numbers (store them?) in some order
# start by placing a "1" in the first non-empty cell and check for violations
# if there are no violations (check constraints - row, column, box), advance to the next spot and fill in a 1
# if there are violations, advance the current number to 2
# keep incrementing until there are no violations
# if all 9 digits can't be in the spot, leave the spot blank, backtrack one spot and increment

# copy this into "board" to start a fresh new board

from timeit import default_timer as currentTime

board = [
    [0, 9, 1, 0, 0, 2, 0, 0, 7],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [6, 0, 2, 4, 0, 0, 0, 0, 0],
    [0, 1, 5, 0, 0, 0, 3, 2, 0],
    [0, 0, 9, 0, 0, 0, 4, 0, 0],
    [0, 3, 4, 0, 0, 0, 6, 7, 0],
    [0, 0, 0, 0, 0, 7, 2, 0, 3],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [1, 0, 0, 3, 0, 0, 8, 9, 0]
]

boardblank = [
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

def getinput():
    stringin = input("input your sudoku board in one continous string \nwhere blank spaces are zero, lines are separated by commas, any trailing zeros can be left out\n e.g _ 1 5 _ 3 2 _ _ _ becomes 015032,\n")
    stringin.replace(" ", "") # remove spaces
    stringin=list(stringin)
    for i in range(len(stringin)):
        if not(stringin[i].isdigit() or stringin[i] == ","): # replace characters that aren't numbers or spaces with 0
            stringin[i] = "0"

    stringin = "".join(stringin)
    stringin = stringin.split(",") # each string of numbers is now its own element
    board = []
    for i in range(len(stringin)):
        row = list(stringin[i])
        while len(row) != 9:
            if len(row) < 9:
                row.append(0)
            if len(row) > 9:
                row.pop(-1)
        row = [int(x) for x in row]
        board.append(row)
    while len(board) != 9:
        if len(board) < 9:
            board.append([0,0,0,0,0,0,0,0,0])
        if len(board) > 9:
            board.pop(-1)
    return board
    
    
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
        if f % 1000000 == 0:
            print(f"{f:,} iterations so far.")
        if board[cRow][cCol] + 1 < 10:
            board[cRow][cCol] += 1
            if isValid(board, [cRow, cCol], board[cRow][cCol]):
                return True
        elif emptyPos == 0:
            return None
        else:
            board[cRow][cCol] = 0
            emptyPos -= 1
            cRow, cCol = empties[emptyPos]
            

def solve(board):
    global solutions
    solutions = []
    empties = findEmpties(board)
    # check to see if starting position is valid
    for i in range(9):
        for j in range(9):
            if not isValid(board, (i, j), board[i][j]):
                return None
    if len(empties) == 0: # board is already solved
        solutions.append([row[:] for row in board])
        return solutions
    while True:
        cRow = None
        cCol = None
        for i, j in empties: # find our next empty cell
            if board[i][j] == 0:
                cRow = i
                cCol = j
                break # break the loop if we find it

        # if the previous loop didn't assign a value to cRow and cCol,
        # we know there are no more empty cells left on the board and
        # we have found a solution
        if cRow is None and cCol is None:
            solutions.append([row[:] for row in board])
            cRow, cCol = empties[-1]
            
        if backtrack(board, empties, (cRow, cCol)) == None: # If backtracking broke down, we've found all valid solutions.
            break
    return solutions

def print_solutions(solutions, recursive=False):
    if not solutions:
        print("\nNo solution exists")
        return
    
    if not recursive:
        print(f"\n{len(solutions)} solution{'s' if len(solutions) > 1 else ''} found.\n")
    if len(solutions) > 3 and not recursive:
        print(f"First three solutions:\n")
        sols = 0
        for sol in solutions:
            solu = (sol,)
            print_solutions(solu, True)
            sols += 1
            if sols >= 3:
                return
    for solution in solutions:
            for i in range(len(solution)):
                if i % 3 == 0 and i != 0:
                    print("- - - - - - - - - - - - - ")

                for j in range(len(solution[0])):
                    if j % 3 == 0 and j != 0:
                        print(" | ", end="")

                    if j == 8:
                        print(solution[i][j])
                    else:
                        print(str(solution[i][j]) + " ", end="")
            print("\n")
command_line = False
def main():
    global f
    loop = True
    while loop:
        if command_line:
            board_unsolved = getinput()
        else:
            loop = False
            board_unsolved = board

        f = 0 # iteration counter

        startTime = currentTime()

        solutions = solve(board_unsolved)
        timeToComplete = currentTime() - startTime
        print_solutions(solutions)

        print(f"{f} iterations to fully solve this puzzle") if f != 0 else print()

        print(f"took {timeToComplete} seconds to complete\n")
main()
