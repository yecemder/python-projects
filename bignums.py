# big numbers go whee

from sys import set_int_max_str_digits as max_digits

max_digits(2147483647)

arrLen = 1500

def generateArray(length):
    global arr
    arr = []
    for i in range(length):
        arr.append(i+1)

def bogoBogoPredict(array):
    number = 1
    current_factorial = 1
    end = len(array) + 1
    for i in range(1, end):
        current_factorial *= i
        number *= current_factorial
    return number

generateArray(arrLen)
num = bogoBogoPredict(arr)
print("Prediction done. Printing result...\n")
print(num)
