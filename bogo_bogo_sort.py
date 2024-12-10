# Bogobogosort sorts a list as inefficiently as possible
# shuffle the elements of a sublist (starting at n=2 elements)
# if they're arranged correctly, shuffle n+1 elements
# if in incorrect order from shuffle, restart
# continue until sorted

from random import random
from math import floor
from timeit import default_timer as time

def bogoBogoPredict(array):
    """Predicts the average number of shuffles for BBSort to finish.

    Uses formula n! = (n-1)! * n to not waste factorial calculations.
    """
    number = 1
    currentFactorial = 1
    for i in range(1, len(array) + 1):
        currentFactorial *= i
        number *= currentFactorial
    return number

def generateArray(arrayLength):
    """Creates an array consisting of values 1 to arrayLength."""
    return randomizeOrder([i for i in range(1, arrayLength+1)])

def isSorted(array):
    """Checks if a list is sorted."""
    i = 1
    while i < len(array):
        if array[i] < array[i - 1]: 
            return False 
        i += 1
    return True

def randomizeOrder(array):
    """Randomizes the order of a list.

    Uses an improved version of the Fisher-Yates algorithm, performing n-1 shuffles,
    over Python's random.shuffle(), which performs n shuffles.
    """
    shuffleAmnt = len(array)
    while shuffleAmnt > 1:
        i = floor(random() * shuffleAmnt)
        shuffleAmnt -= 1
        if i == shuffleAmnt:
            continue
        array[i], array[shuffleAmnt] = array[shuffleAmnt], array[i]
    return array

def bogoBogoSort(array):
    """Sorts an array using the bogoBogoSort algorithm."""
    tries = 0
    if len(array) < 2:
        return array, tries
    currentIndex = 2
    lenArray = len(array)
    while True:
        tries += 1
        if isSorted(randomizeOrder(array[:currentIndex])):
            if currentIndex == lenArray:
                return array, tries
            currentIndex += 1
        else:
            currentIndex = 2

def main():
    arrLen = 6 # Controls base array length upon generation
    unsorted = generateArray(arrLen)
    print(f"This {arrLen:,}-element array is predicted to take {bogoBogoPredict(unsorted):,} tries to sort on average.\n")
    startTime = time()
    sortedArr, tries = bogoBogoSort(unsorted)
    endTime = time()
    changeTime = endTime - startTime
    print(f"\nThis {arrLen:,}-element array was sorted in {tries:,} tries.")
    print(f"\nTotal time: {changeTime}\nAverage time: {changeTime / tries}")

if __name__ == "__main__":
    main()
