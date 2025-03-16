import time
import cProfile
import math
import timeit
from functools import reduce
from math import factorial

arrLen = 1000 # tweak this value for ridiculous numbers

arr = []
variance = 1000

def bogoBogoPredict(array):
    global number
    number = 1
    global i
    i = 1
    while i <= len(array):
        num = math.factorial(i)
        number *= num
        i += 1
    return number

def bogoBogoPredict2(array):
    number = 1
    for i in range(1, len(array)+1):
        num = math.factorial(i)
        number *= num
    return number

def bogoBogoPredict3(array):
    number = 1
    prevNum = 1
    currentNum = 1
    end = len(array) + 1
    for i in range(1, end):
        currentNum = prevNum * i
        number *= currentNum
        prevNum = currentNum
    return number

def bogoBogoPredict4(array):
    factorial_values = [1]  # Initialize the list with the factorial of 1.
    
    # Calculate and store factorials up to the length of the array.
    for i in range(1, len(array) + 1):
        factorial_values.append(factorial_values[-1] * i)
    # Calculate the predicted number of tries using the stored factorials.
    predicted_tries = 1
    for i in factorial_values:
        predicted_tries *= i

    return predicted_tries

##def bogoBogoPredict5(array):
##    return reduce(lambda x, y: x * y, (math.factorial(i) for i in range(1, len(array) + 1)), 1)

def bogoBogoPredict5(array):
    number = 1
    for i in range(1, len(array)+1):
        number *= math.factorial(i)
    return number

def bogoBogoPredict6(array):
    number = 1
    current_factorial = 1
    end = len(array) + 1
    for i in range(1, end):
        current_factorial *= i
        number *= current_factorial
    return number




##def bogoBogoPredict2(array):
##    number = 1
##    for i in range(len(array)):
##        num = math.factorial(i+1)
##        number *= num
##    return number

def generateArray():
    for i in range(arrLen):
        arr.append(i+1)

generateArray()

iters = 100

##startTime = timeit.default_timer()
##for i in range(iters):
##    num1 = bogoBogoPredict(arr)
##timeTaken = timeit.default_timer() - startTime
##print(f"\nPredicting the tries of an array {iters} times using version 1 of length {arrLen} took {timeTaken} seconds.")
####print(num1)
##
##startTime = timeit.default_timer()
##for i in range(iters):
##    num2 = bogoBogoPredict2(arr)
##timeTaken = timeit.default_timer() - startTime
##print(f"\nPredicting the tries of an array {iters} times using version 2 of length {arrLen} took {timeTaken} seconds.")
####print(num2)
##
##startTime = timeit.default_timer()
##for i in range(iters):
##    num3 = bogoBogoPredict3(arr)
##timeTaken = timeit.default_timer() - startTime
##print(f"\nPredicting the tries of an array {iters} times using version 3 of length {arrLen} took {timeTaken} seconds.")
####print(num3)
##
##startTime = timeit.default_timer()
##for i in range(iters):
##    num4 = bogoBogoPredict4(arr)
##timeTaken = timeit.default_timer() - startTime
##print(f"\nPredicting the tries of an array {iters} times using version 4 of length {arrLen} took {timeTaken} seconds.")
####print(num4)
##
startTime = timeit.default_timer()
for i in range(iters):
    num5 = bogoBogoPredict5(arr)
timeTaken = timeit.default_timer() - startTime
print(f"\nPredicting the tries of an array {iters} times using version 5 of length {arrLen} took {timeTaken} seconds.")
##print(num5)

startTime = timeit.default_timer()
for i in range(iters):
    num6 = bogoBogoPredict6(arr)
timeTaken = timeit.default_timer() - startTime
print(f"\nPredicting the tries of an array {iters} times using version 6 of length {arrLen} took {timeTaken} seconds.")
##print(num6)


##print(f"Printing results...")
##print(f"Predicted to take {num1} tries.")
##startTime = timeit.default_timer()
##num2 = bogoBogoPredict2(arr)
##print(f"2nd version took {timeit.default_timer() - startTime} seconds.")
