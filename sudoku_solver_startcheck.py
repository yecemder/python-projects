from timeit import default_timer as time

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

board1 = [ # this serves no purpose other than to be copy-pasted into "board" to reset it.
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

use_command_line = False

def ic(s): # Function to convert sudopedia puzzles into command-line inputs
    return ','.join([s[i:i+9] for i in range(0, len(s), 9)])

def getinput():
    # Get a user input on the command line, and output a 2D array with dimensions 9x9 for a sudoku board.
    
    stringin = input("input your sudoku board in one continous string \nwhere blank spaces are zero, lines are separated by commas \nany trailing zeros can be left out\n e.g _ 1 5 _ 3 2 _ _ _ becomes 015032,\n")

    stringin.replace(" ", "") # Remove spaces
    stringin=list(stringin) # Convert to list to make mutable
    for i in range(len(stringin)):
        if not(stringin[i].isdigit() or stringin[i] == ","): # replace characters that aren't numbers or spaces with 0
            stringin[i] = "0"

    stringin = "".join(stringin) # Turn list back into a string. 
    stringin = stringin.split(",") # Turn each string of numbers into its own element of an array, where each split occurs at commas
    
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
    # Find all empty cells in the board and store their locations as tuples (row, col) into a list.
    return [(row, col) for row in range(9) for col in range(9) if board[row][col] == 0]

def isValid(board, pos, num):
    # Checks if a number is contained in the same row, column, or box as the position given.
    # Returns False if a duplicate is found, or True otherwise.
    row, col = pos
    
    # Check if the same number as num is in the same row
    if num in board[row]:
        return False

    # Ditto for cols
    for i in range(9):
        if board[i][col] == num:
            return False

##    if any(board[i][col] == num for i in range(9)):
##        return False
##    if num in [board[i][col] for i in range(9)]:
####    if num in col_vals:
##        return False

    # Figure out in which box the position of the number falls, and
    # check those boxes.

##    boxX, boxY = col // 3, row // 3
##    for i in range(boxY*3, boxY*3+3):
##        for j in range(boxX*3, boxX*3+3):
            
    boxStartX, boxStartY = col // 3 * 3, row // 3 * 3
    for i in range(boxStartY, boxStartY+3):
        for j in range(boxStartX, boxStartX+3):
            
            if board[i][j] == num:
                return False
            
##    # not that bad, but still creates whole new list
##    box_values = [board[i][j] for i in range(boxY*3, boxY*3+3) for j in range(boxX*3, boxX*3+3)]
##    return all(x != num for x in box_values)
##
##    # genexprs are slower with any(), bc they don't short circuit
##    return not (any(board[i][j] == num for i in range(boxY*3, boxY*3+3) for j in range(boxX*3, boxX*3+3)))
##
##    # Redundant calculations
##    for i in range(9):
##        if board[boxY * 3 + i // 3][boxX * 3 + i % 3] == num:
##            return False
##    # Ditto
##    for i in range(3):
##        for j in range(3):
##            if board[boxY * 3 + i][boxX * 3 + j] == num:
##                return False
##
##    # Creates whole new list
##    box = [board[i][j] for i in range(boxY*3, boxY*3+3) for j in range(boxX*3, boxX*3+3)]
##    if num in box:
##        return False

    # If we passed all checks, the spot must be valid.
    return True

##def isValid(board, pos, num):
##    row, col = pos
##    row_vals = {board[row][i] for i in range(9)}
##    if num in row_vals:
##        return False
##    col_vals = {board[i][col] for i in range(9)}
##    if num in col_vals:
##        return False
##    boxX, boxY = col // 3, row // 3
##    for i in range(9):
##        box_row, box_col = boxY * 3 + i // 3, boxX * 3 + i % 3
##        if board[box_row][box_col] == num:
##            return False
##    return True

def startCheck(board, pos, num):
    # Specialized function to only check starting position where the number we're checking will definitely
    # be in the board, so it needs to also check if the spot we're currently checking is also the spot
    # it found a duplicate number.
    # Separating the functions into two means we don't have to do a check if we're looking at
    # the board itself or a proposed number.
    
    if num == 0: # If the number is blank, it's obviously valid.
        return True

    row, col = pos
    
    # If we fail any of the checks, it's not a valid spot for the number.

    # Check if the same number as num is in the same column, ignoring
    # the spot we're currently checking.
    for i in range(9):
        if i != col and board[row][i] == num:
            return False

    # Ditto for rows.
    for i in range(9):
        if i != row and board[i][col] == num:
            return False

    # Figure out in which box the position of the number falls, and
    # check those boxes.
    
    boxX, boxY = col // 3, row // 3
    for i in range(boxY*3, boxY*3+3):
        for j in range(boxX*3, boxX*3+3):
            if (i, j) != pos and board[i][j] == num:
                return False

    # If we passed all checks, the spot must be valid.
    return True

def backtrack(board, empties):
    global iters
    solutions = []
    
    # If the board is already full, we can't solve it.
    if len(empties) == 0: 
        solutions.append([row[:] for row in board])
        return solutions
    
    # Start at beginning of the list of empty cells.
    emptyPos = 0
    row, col = empties[0]
    num = 0
    while True:
        iters += 1
        if num < 9:
            num += 1
            if isValid(board, (row, col), num):
                # If the number works, write it to the board
                board[row][col] = num
                
                # If we reached the end of the llist of empties,
                # make a copy of the board, append it to the list of solutions,
                # and keep going.
                if emptyPos + 1 == len(empties):
                    solutions.append([across[:] for across in board])
                    continue
                else:
                    emptyPos += 1 # Advance one empty
            
            else:
                # If the number wasn't valid, go back and try another.
                continue
                
        # If there are no valid numbers in the current position and
        # we're at the beginning, then we can't find any more solutions.
        elif emptyPos == 0:
            return solutions

        # If no number up to 9 was valid, move back a space and set the
        # current space back to blank.
        else:
            board[row][col]= 0
            emptyPos -= 1

        # Reassign the current working row, column based on any increments or decrements
        # made to emptyPos, which indicates that we need to move forward or back.
        row, col = empties[emptyPos]
        num = board[row][col]
    

def solve(board):

    # Check if starting position is invalid
    for row in range(9):
        for col in range(9):
            if not startCheck(board, (row, col), board[row][col]):
                return None

    # Find empty squares
    empties = findEmpties(board)

    # Run backtracking to solve board
    return backtrack(board, empties)

def print_solutions(solutions):
    
    if solutions is None: # If solutions returned none, the starting configuration was invalid
        print("Conflicts in starting position found, invalid position.")
        return
    
    if not solutions: # If solutions is empty
        print("No solution exists.")
        return
    
    print(f"{len(solutions)} solution{'s' if len(solutions) > 1 else ''} found.\n")
    
    # We don't want to print more than 3 solutions (too much to print, no one cares, etc.)
    if len(solutions) > 3: 
        print(f"First three solutions:\n")
        # Only have the first 3 solutions be printed
        solutions = solutions[:3]

    # Print the solutions.
    for solution in solutions:
        print_board(solution)

def print_board(board):
    # Function to print a sudoku board represented as a 2D array to console.
    
    for i in range(len(board)):

        # After every third row, print a horizontal line.
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")

        for j in range(len(board[0])):
            
            # After every third column, print a part of the vertical lines.
            if j % 3 == 0 and j != 0:
                print("| ", end="")

            # Get the number to print. If blank, print a dot instead for readibility.
            number = str(board[i][j]) if board[i][j] != 0 else "·"

            # If the number is the last in the list, print it normally (with newline).
            if j == 8:
                print(number)
            # Otherwise, don't print it with a new line.
            else:
                print(number, end=" ")
    print()

def main():
    global iters
    loop = True
    while loop:
        # This if-else statement is the equivalent of a do-while loop -
        # "do (solve then print board) while command line is true"
        # Copies the desired board to be solved into "board_unsolved"
        # so we can still access the original input.
        if use_command_line:
            board_unsolved = getinput()
        else:
            loop = False
            board_unsolved = board
        print(f"\nInput board:\n")
        print_board(board_unsolved)

        iters = 0 # iteration counter

        startTime = time()

        solutions = solve(board_unsolved)
        timeToComplete = time() - startTime
        print_solutions(solutions)

        print(f"{iters} iterations to fully solve this puzzle") if iters != 0 else print()

        print(f"took {timeToComplete} seconds to complete\n")

main()
