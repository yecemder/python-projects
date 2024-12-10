from math import log10, floor
from timeit import default_timer as time

def initialguess(x):
    digits = floor(log10(x))+1

    if digits % 2 == 1:
        digits += 1

    return 3*10**(digits-1)

def bab_sr(x):
    if x < 0:
        return
    if x == 0:
        return 0

    tol = 1 / (10 ** 10)

    maxiters = 50
    # guess = initialguess(x)
    guess = x / 2
    prevGuess = guess
    for i in range(maxiters):
        guess = (guess + (x/guess))/2
        if abs(guess-prevGuess) < tol:
            #print(i)
            return guess
        prevGuess = guess
    return guess


startTime = time()
bab_sr(1000)
timeTaken = time() - startTime
print(timeTaken)
