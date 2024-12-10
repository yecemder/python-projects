# solve_for_x testing
from math import *

def evaluate(expression, x):
    return eval(expression)

def main():
    ex = "2*sin(x)"

    result = evaluate(ex, 2)
    print(result)

main()

def makeGuesses(equation):
    vals = []
    for i in initials:
        try:
            res = evaluate(equation, i)
            vals.append(res)
        except:
            vals.append(None)
    for i in range(len(vals)):
        if vals[i] == 0:
            return initials[i], True
##    for i in range(len(vals)-1):
##        # Ignore undefined values
##        if vals[i] == None: continue
##
##        # If there's a sign change, there must be a zero im between the two current values.
##        sgn2 = sgn(vals[i+1])
##        if (sgn(vals[i]) != sgn2) and (sgn2 != None):
##            return (initials[i]+initials[i+1]) / 2, False # Return their average

    # Use the value that comes closest to zero.
    lowest_val = float('inf')
    lowest_index = -1
    
    for i in range(len(vals)):
        if vals[i] == None: continue # Ignore undefined
        
        if abs(vals[i]) < abs(lowest_val):
            lowest_val = vals[i]
            lowest_index = i
            
    return initials[i], False
