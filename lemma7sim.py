# ratio approximations of a number with integers
from math import sqrt, pi, e
from timeit import default_timer as time
# desired number to approximate
number = 50000/399

maxval = 1_000_000
def approx():
    c1, c2 = 1, 1
    best = (c1, c2)
    lowest = float('inf')
    final = (0, 0)
    found_lowests = []
    for _ in range(maxval*2):
        ratio = c1/c2
        result = abs(number - (ratio))
        if result < lowest:
            lowest = result
            found_lowests.append((c1, c2))
            best = (c1, c2)
        if ratio < number:
            c1 += 1
        elif ratio > number:
            c2 += 1
        else:
            break
        if c1 > maxval or c2 > maxval:
            break
    return best, lowest, found_lowests
        
def printout(best, low, found):
    print(f'number: {number} \napprox: {best[0]/best[1]} \nbest approximation: {best[0]}/{best[1]} ({low})')
    print()
    print("best found approximations:", end=" ")
    s = ", ".join([f"{str(a)}/{str(b)}" for a, b in found])
    print(s)
##    for i in range(len(found)):
##        print(f"{found[i][0]}/{found[i][1]}", end="")
##        if not(i == len(found)-1):
##            print(", ", end = "")
    print("\n")

def main():
    start = time()
    best, low, found = approx()
    timetaken = time()-start
    printout(best, low, found)
    print(f"took {timetaken} seconds to finish")

main()
