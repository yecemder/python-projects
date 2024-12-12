from random import randint
from time import sleep
import sys
color = sys.stdout.shell

def type(message):
    for char in message:
        print(char, end="")
        sleep(0.02)
    print()
        
while True:
    diff = input("\n\nWould you like to play Battleship in Easy, Hard, or Expert?\n\n").lower().strip()
    if diff == "easy":
        numDifficulty = 5
        break
    elif diff == "hard":
        numDifficulty = 15
        break
    elif diff == "expert":
        numDifficulty = 25
        break
    else:
        print("That's not a valid difficulty!")
        
print()

SIZE = 10
FINALLETTER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SHIPSYMBOL = "@#&$%" # Carrier, Battleship, Cruiser, Submarine, Destroyer
SHIPLENGTH = [5,4,3,3,2]

def printBoard(board):
    #print header
    print("  ",end="")
    for i in range(SIZE):
        color.write(chr(i+65)+" ", "DEFINITION")
    print()
    
    for i in range(SIZE):
        color.write(chr(i+48)+" ", "DEFINITION")
        for j in range(SIZE):
            color.write(board[10*i+j]+" ", "BUILTIN")
        color.write(""+chr(i+48)+"\n", "DEFINITION")

    print("  ",end="")
    for i in range(SIZE):
        color.write(chr(i+65)+" ", "DEFINITION")
    print()

def convertToIndex(choice):
    return int(choice[1])*SIZE+(ord(choice[0])-65)
def convertToCoord(choice):
    return chr(choice%10+65)+str(choice//10)
def convertToShipH(choice):
    return SHIPSYMBOL.index(choice)

def placeShip(x, y, o, size, board, symbol):
    if(size == 0):
        return True
    t = (y+o*(size-1))*SIZE+(x+(size-1)*(1-o))
    if( t<0 or t>=SIZE*SIZE or (o==0 and size>1 and (t-1)%SIZE > t%SIZE)):
        return False
    if(board[t]=="·" and placeShip(x,y,o,size-1,board,symbol)):
        board[t] = symbol
        return True
    return False

def randPlaceShip(board):
    for i in range(5):
        while(True):
            x = randint(0,SIZE-1)
            y = randint(0,SIZE-1)
            o = randint(0,1)
            if(placeShip(x,y,o,SHIPLENGTH[i],board, SHIPSYMBOL[i])):
                break

def getValidInput(board):
    while(True):
        user = input("Enter a position to test: ").upper()
        if(len(user)==2):
            if("A"<=user[0] and user[0]<=FINALLETTER[SIZE] and "0"<=user[1] and user[1]<="9"):
                t = convertToIndex(user)
                if(board[t]=="·"):
                    return t
                else:
                    print("...that position has already been tested\n")
            else:
                print("...coordinates out of bounds\n")
        else:
            print("...invalid inputs\n")

          
def compChoose(board, last):
    while(True):
        t = randint(0,SIZE*SIZE-1)
        if(board[t]=="·"):
            return t

def compChooseProb(last, chanceHit):
    while True:
        t = randint(1, 100)
        if t <= chanceHit:
            while True:
                n = randint(0,SIZE*SIZE-1)
                if mine[n] in SHIPSYMBOL and compMove[n] == "·":
                    return n
        else:
            while True:
                n = randint(0,SIZE*SIZE-1)
                if mine[n] not in SHIPSYMBOL and compMove[n] == "·":
                    return n
            

def isHit(board, target):
    return board[target] in SHIPSYMBOL

def tShipHit(board, move): # gets type of ship hit, added
    t = board[move]
    return t
    
comp = ["·"]*(SIZE**2)
compMove = ["·"]*(SIZE**2)
compShipHealth = [x for x in SHIPLENGTH]
compShips = 5
cp = -1
randPlaceShip(comp)

mine = ["·"]*(SIZE**2)
mineMove = ["·"]*(SIZE**2)
mineShipHealth = [x for x in SHIPLENGTH]
mineShips = 5
my = -1
randPlaceShip(mine)

while(True):
    color.write(" "*7 + "OPPONENT"+"\t\tships sunk: "+str(5-compShips)+"\n", "COMMENT")
    printBoard(mineMove)
    print()
    printBoard(mine)
    color.write(" "*9 + "MINE"+"\t\tships left: "+str(mineShips)+"\n", "STRING")
    print()
    
    # beginning of vaughn
    
    my = getValidInput(mineMove)
    if isHit(comp, my):
        color.write("...That was a hit!\n\n", "STRING")
        sleep(1)
        shipHit = tShipHit(comp, my)
        locShipHit = SHIPSYMBOL.index(shipHit)
        SHIPLENGTH[locShipHit] -= 1
        mineMove[my] = "X"
        comp[my] = "X"
        if SHIPLENGTH[locShipHit] == 0:
            compShips -= 1
            color.write("You sunk my ship!\n\n", "STRING")
    else:
        color.write("...splash\n\n", "COMMENT")
        sleep(1)
        mineMove[my] = " "
        comp[my] = " "
    if compShips == 0:
        color.write("You won!\n", "STRING")
        color.write(" "*7 + "OPPONENT"+"\t\tships sunk: "+str(5-compShips)+"\n", "STRING")
        printBoard(comp)
        break
    else:
        cp = compChooseProb(cp, numDifficulty)
        compCoord = convertToCoord(cp)
        type("The computer tested " + str(compCoord) + "...")
        sleep(1)
        if isHit(mine, cp):
            color.write("...And hits!\n\n", "STRING")
            sleep(0.5)
            shipHit = tShipHit(mine, cp)
            locShipHit = SHIPSYMBOL.index(shipHit)
            SHIPLENGTH[locShipHit] -= 1
            mine[cp] = "X"
            compMove[cp] = "X"
            if SHIPLENGTH[locShipHit] == 0:
                mineShips -= 1
                color.write("They sunk your ship!\n", "STRING")
        else:
            color.write("...And misses.\n\n", "COMMENT")
            sleep(0.75)
            compMove[cp] = " "
            mine[cp] = " "
    if mineShips == 0:
        color.write("You lost!\n", "COMMENT")
        print(mine)
        color.write(" "*9 + "MINE"+"\t\tships left: "+str(mineShips)+"\n", "COMMENT")
            
            
        
        
        
        
        
        
        
        
        
