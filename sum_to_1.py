import random
import math

iterations = 10000000

attemptsSum = 0

def percentDifference(num1, num2):
    numerator = abs(num1 - num2)
    denominator = (num1 + num2) / 2
    return (numerator / denominator) * 100
def truncate(number, digits) -> float:
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper



for i in range(iterations):
    sums = 0
    attempts = 0
    while sums <= 1:
        attempts += 1
        num = random.uniform(0, 1)
        sums += num
    attemptsSum += attempts
    if i % 100000 == 0:
        print(f"{i:,} of {iterations:,} trials done.")
        

averageAttempts = attemptsSum / iterations

print(f"\nIt took an average of {truncate(averageAttempts, 8)} trials to achieve a sum of 1, and should have been {truncate(math.e, 8)} which makes it off by {truncate(percentDifference(averageAttempts, math.e), 5)}%.")
