import math
import random
from timeit import default_timer as time

attempts = 1000

candidateNumber = 1000

numBestFound = 0
numInCutoff = 0
numCutEarly = 0

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

beg = time()

for j in range(attempts):
    measuredStat = []

    # create a list of measurable statistics in meaasuredStat
    for i in range(candidateNumber):
        num = random.uniform(0, 150)
        measuredStat.append(num)

    cutoff = candidateNumber // math.e

    cutoff = int(cutoff)

    highCutoff = 0
    # find our cutoff from initial group
    for i in range(cutoff):
        if measuredStat[i] > highCutoff:
            highCutoff = measuredStat[i]

    # find our new candidate from those remaining
    remaining = candidateNumber - int(cutoff)
    foundCandidate = 0
    bestCandidateStat = 0
    for i in range(remaining):
        if measuredStat[i+int(cutoff)] > highCutoff:
            foundCandidate = i+int(cutoff)
            foundCandidateStat = measuredStat[i+int(cutoff)]


    # check if we got the best option
    bestCandidate = 0 
    bestCandidateStat = 0
    i = 0
    while i < len(measuredStat):
        if measuredStat[i] > bestCandidateStat:
            bestCandidateStat = measuredStat[i]
            bestCandidate = i
        i += 1

    if bestCandidate == foundCandidate:
        numBestFound += 1
    elif bestCandidate != foundCandidate and bestCandidate <= cutoff:
        numInCutoff += 1
    elif bestCandidate != foundCandidate and bestCandidate > cutoff:
        numCutEarly += 1
end = time()
duration = int((end-beg)*1000000)

##    if (j+1) % (attempts // 100) == 0:
##        percentDone = ((j+1) / attempts) * 100
##        print(f"{j+1:,} of {attempts:,} trials done. ({truncate(percentDone, 2)}%)")

successRate = (numBestFound / attempts) * 100
expectedRate = (1 / math.e) * 100
print(f"\nOverall, we got the best candidate {numBestFound:,} times. The best candidate was in the initial cuts {numInCutoff:,} times, and we picked the person too early {numCutEarly:,} times. \nOverall, there was a {truncate(successRate, 3)}% success rate based on Euler's number, and we expected a {truncate(expectedRate, 3)}% success rate, which was off by {truncate(percentDifference(successRate, expectedRate), 3)}%.")
print()
print(f"Took {duration} microseconds.")

