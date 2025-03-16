from time import sleep
from random import randint
board = [" "] * 9
winLines = ([0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6])
# ----------------- FUNCTIONS --------------------

def printBoardTemp():
    rows = ([0, 1, 2], [3, 4, 5], [6, 7, 8])
    for i in rows:
        print()
        for j in i:
            print(board[j], end=" ")

def printBoardAttempt():
    rows = ([0, 1, 2], [3, 4, 5], [6, 7, 8])
    s = 0
    for i in rows:
        print()
        t = 0
        for j in i:
            print(board[j], end="")
            if t < 2:
                print("\t|\t", end="")
            t += 1
        print()
        if s <= 1:
            print("_"*33)
        s += 1

def determineWinner():
    tieCheck = 0
    for i in winLines:
        if board[i[0]] == board[i[1]] and board[i[0]] == board[i[2]]:
                if board[i[0]] != " ":
                    return board[i[0]]
    for j in board:
        if j == "X" or j == "O":
            tieCheck += 1
    if tieCheck == 9:
        return False
    return None

def getValidInput():
    while True:
        user = input("\nEnter the position you want to play your move (1-9): ").strip()
        try:
            user = int(user)
        except ValueError:
            print("Invalid input.")
        else:
            if user >= 1 and user <= 9:
                user -= 1
                if board[user] != "X" and board[user] != "O":
                    return user
                else:
                    print("That position is already taken.")
            else:
                print("Input not in range!")

def compMove():
    while True:
        comp = randint(0, 8)
        if board[comp] != "X" and board[comp] != "O":
            return comp

def compMoveSmart():
    for i in winLines: # check for win moves
        oCount = 0
        for j in i:
            if board[j] == "O": # checks winLines for things with 2 o's
                oCount += 1
        if oCount == 2: # if the computer is about to win because it has 2 o's in a winline
            for j in i:
                if board[j] != "X" and board[j] != "O": # if the spot's available,
                    return j # move to win
                
    for i in winLines: # check if its about to lose
        xCount = 0
        for j in i:
            if board[j] == "X": # checks winLines for anything that has 2 x's, meaning you're about to lose
                xCount += 1
        if xCount >= 2: # if the computer is about to lose
            for j in i:
                if board[j] != "X" and board[j] != "O": # if the spot's available, 
                    return j # move to avoid losing
    
    ideals = (4, 0, 2, 8, 6) # move in center then corners CCW from the top left
    for i in ideals:
        if board[i] != "X" and board[i] != "O": # if its available
            return i # move in ideal area
        
    while True: # if none of the above conditions are satisfied (no winlines, no loselines, no ideal spots available)
        comp = randint(0, 8) # pick random spot
        if board[comp] != "X" and board[comp] != "O":
            return comp


        
# ----------------- CODE ------------------
def main():
    while True:
        printBoardAttempt()
        pMove = getValidInput()
        board[pMove] = "X"
        if determineWinner() is False:
            print("\nIt's a tie!\n")
            break
        elif determineWinner() is not None:
            print("\nThe winner is "+determineWinner()+"!\n")
            printBoardAttempt()
            break
        comp = compMoveSmart()
        board[comp] = "O"
        if determineWinner() is False:
            print("\nIt's a tie!\n")
            break
        elif determineWinner() is not None:
            print("\nThe winner is "+determineWinner()+"!\n")
            printBoardAttempt()
            break
    
if __name__ == "__main__":
    main()
