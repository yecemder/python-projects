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

board1 = [ # this serves no purpose other than to be copy-pasted into "board" to reset it.
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

use_command_line = True

def ic(s):
    return ','.join([s[i:i+9] for i in range(0, len(s), 9)])

def getinput():
    # Get a user input for "board" on the command line.
    
    stringin = input("input your sudoku board in one continous string \nwhere blank spaces are zero, lines are separated by commas, any trailing zeros can be left out\n e.g _ 1 5 _ 3 2 _ _ _ becomes 015032,\n")
    stringin.replace(" ", "") # remove spaces
    stringin=list(stringin)
    for i in range(len(stringin)):
        if not(stringin[i].isdigit() or stringin[i] == ","): # replace characters that aren't numbers or spaces with 0
            stringin[i] = "0"

    stringin = "".join(stringin) # Turn list back into string. 
    stringin = stringin.split(",") # Turn each string of numbers into its own element of an array.
    board = [] # Initialize our return value.

    # For each element in our array, correct it and add it to "board".
    for i in range(len(stringin)):

        # Grab what we want to append and turn it into a list
        row = list(stringin[i])

        # If we don't have 9 elements, remove numbers or add blanks to the end.
        while len(row) != 9:

            # If we don't have enough elements, add a blank at the end.
            if len(row) < 9:
                row.append(0)

            # If we have too many, remove one from the end. 
            if len(row) > 9:
                row.pop(-1)

        # Turn the list of single numbers as strings into a list of ints and append it to the output.
        row = [int(x) for x in row]
        board.append(row)
        

    # If we don't have 9 rows, remove rows or add blank ones at the end.
    while len(board) != 9:

        # Too few means we need to add a row.
        if len(board) < 9: 
            board.append([0,0,0,0,0,0,0,0,0])

        # Too many means we need to remove one.
        if len(board) > 9:
            board.pop(-1)

    return board
    
    
def findEmpties(board):
    empties = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
    return empties


def isValid(board, pos, num):

    row, col = pos
    
    # If we fail any of the checks, it's not a valid spot for the number.

    # Check if the same number as num is in the same column, ignoring
    # the spot we're currently checking.
    for i in range(9):
        if board[row][i] == num:
            return False

    # Ditto for rows.
    for i in range(9):
        if board[i][col] == num:
            return False

    # Figure out in which box the position of the number falls, and
    # check those boxes.
    
    boxX, boxY = col // 3, row // 3
    for i in range(boxY*3, boxY*3+3):
        for j in range(boxX*3, boxX*3+3):
            if board[i][j] == num:
                return False

    # If we passed all checks, the spot must be valid.
    return True

def backtrack(board, empties):
    global f
    solutions = []
    
    # If the board is already full, we can't make any changes.
    if len(empties) == 0: 
        solutions.append(board)
        return solutions
    
    # Start at beginning of the list of empty cells.
    emptyPos = 0
    row, col = empties[0]
    num = board[row][col]
    
    while True:
        f += 1 # Increment iteration counter
        if num < 9:
            # If the working number is less than 9 (meaning we can add 1 to it),
            # add 1 to it and check if it is a valid input.
            num += 1
            if isValid(board, (row, col), num):
                # If the number works, write it to the board
                board[row][col] = num
                
                if emptyPos + 1 == len(empties): # at the end of the empties
                    solutions.append([row[:] for row in board])
                    continue
                else:
                    emptyPos += 1 # advance one empty
            
            else:
                # If the number wasn't valid, go back and try another
                continue
                
        elif emptyPos == 0:
            return solutions # broke down
        else:
            # If no number up to 9 was valid, move back a space and set the
            # current space back to blank.
            board[row][col] = 0
            emptyPos -= 1
        row, col = empties[emptyPos]
        num = board[row][col]
    
    

def solve(board):
    empties = findEmpties(board)
    return backtrack(board, empties)

def print_solutions(solutions):
    if solutions == None:
        print("Invalid starting position.")
        return
    
    if not solutions:
        print("No solution exists.")
        return
    
    print(f"\n{len(solutions)} solution{'s' if len(solutions) > 1 else ''} found.\n")
    
    # We don't want to print more than 3 solutions (too much to print, no one cares, etc.)
    if len(solutions) > 3: 
        print(f"First three solutions:\n")
        # Only have the first 3 solutions to be printed
        solutions = solutions[:3]

    for solution in solutions:
        print_board(solution)

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            number = board[i][j] if board[i][j] != 0 else "·"
            if j == 8:
                print(number)
            else:
                print(str(number) + " ", end="")
    print("\n")

def main():
    global f
    loop = True
    while loop:
        # this if-else statement is the equivalent of a do-while loop -
        # "do solve and print board while command line is true"
        if use_command_line:
            board_unsolved = getinput()
        else:
            loop = False
            board_unsolved = board
        print(f"\nInput board:\n")
        print_board(board_unsolved)

        f = 0 # iteration counter

        startTime = currentTime()

        solutions = solve(board_unsolved)
        timeToComplete = currentTime() - startTime
        print_solutions(solutions)

        print(f"{f} iterations to fully solve this puzzle") if f != 0 else print()

        print(f"took {timeToComplete} seconds to complete\n")

main()
