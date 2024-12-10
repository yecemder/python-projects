import time
import datetime
from random import randint
from numpy import inf
import math
# PURPOSE: continually generate random numbers within a list, note the number of duplicates found in trying to get every possible number with random generation, average it out

dupesList = []
pulledList = []

# parameters for trials
goThroughs = 100 # total trials; more trials, higher accuracy, longer load time
totalPosb = 1624 # distinct possibilities

lowestTrial = float(inf)
highestTrial = float(-inf)

consolePrintFrequency = 10

def truncate(number, digits) -> float:
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

print(f"with output to console every consolePrintFrequency. running... \n")

presentDate = datetime.datetime.now()
unix_timestamp = datetime.datetime.timestamp(presentDate)


for i in range(goThroughs):
    foundNumbers = []
    dupes = 0
    numsPulled = 0
    while True:
        newNum = randint(1,totalPosb)
        numsPulled += 1
        if newNum not in foundNumbers:
            foundNumbers.append(newNum)
        else:
            dupes += 1
        if len(foundNumbers) >= totalPosb:
            break
    pulledList.append(numsPulled)
    dupesList.append(dupes)
    if len(dupesList)%consolePrintFrequency == 0:
        print(f"{len(dupesList)} of {goThroughs} trials done.")
    if dupes < lowestTrial:
        lowestTrial = dupes
    elif dupes > highestTrial:
        highestTrial = dupes


presentDate = datetime.datetime.now()
unix_timestamp2 = datetime.datetime.timestamp(presentDate)



# average number of dupes over all trials
totalDupes = 0
for i in dupesList:
    totalDupes += int(i)
dupeAvg = totalDupes // goThroughs

totalPulled = 0
for i in pulledList:
    totalPulled += int(i)
pullAvg = totalPulled // goThroughs



timeToExec = abs(unix_timestamp2 - unix_timestamp)
tteAvg = timeToExec / goThroughs

pullsPerSec = totalPulled / timeToExec

timeToExec = truncate(timeToExec, 6)
tteAvg = truncate(tteAvg, 6)

print(f"\nAverage pulls per second (best measure of speed per cycle to pull a possibility): {pullsPerSec}\n")
print(f"Took {timeToExec} seconds to execute, with an average of {tteAvg} seconds per trial. \n")
print(f"Based on {totalPosb} possiblilities, {dupeAvg} duplicates were found on average before finding all numbers with {pullAvg} average pulls. \n{goThroughs} total trials were attempted, with {totalPulled} pulls and {totalDupes} overall duplicates found. \nThe highest trial had {highestTrial} duplicates, and the lowest trial had {lowestTrial} dupes.")
