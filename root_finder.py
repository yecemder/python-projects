from math import sqrt, inf
from timeit import default_timer as time
from decimal import Decimal, getcontext

# Number of decimal places to use in calculations
getcontext().prec = 50

def superscript(n):
    out = ""
    while(n>0):
        v = n%10
        if(v==1):
            out = "\u00b9" + out
        elif(v==2 or v==3):
            out = chr(ord("\u00b0")+v) + out
        else:
            out = chr(ord("\u2070")+v) + out
        n //= 10
    return out

def mkTerm(coeff, deg):
    if coeff == 0 or deg < 0:
        return
    coeff = abs(coeff)
    x = ""
    if deg >= 1:
        x = "x"
    out = ""
    if (x == "x" and coeff != 1) or x == "":
        out += str(round(coeff, 4))
    out += x
    if deg > 1:
        out += superscript(deg)
    return out
        

def formatPoly(coeffs):
    coeffs = [float(i) for i in coeffs]
    out = ""
    outList = []
    try:
        ints = list(map(lambda x: int(x), coeffs))
    except:
        return "Input issue: couldn't create an expression from input."
    if coeffs == [0] or coeffs == []:
        return "0"

    for i in range(len(coeffs)):
        if coeffs[i] == int(coeffs[i]):
            coeffs[i] = int(coeffs[i])

    for i in range(len(coeffs)):
        if coeffs[i] < 0:
            t = mkTerm(coeffs[i], i)
            if t is not None:
                outList.append("-" + t)
        else:
            t = mkTerm(coeffs[i], i)
            if t is not None:
                outList.append(t)
                
    outList.reverse()
    for i in range(len(outList)):
        if outList[i] is not None:
            out += str(outList[i])
            if i < len(outList) - 1:
                out += " + "

    out = list(out)
    for i in range(len(out)):
        if out[i] == "+" and out[i+1] == " " and out[i+2] == "-":
            out[i] = "-"
            out[i+2] = ""
            
    return "".join(out)

def trimcoeffs(coeffs):
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop(-1)
    coeffs = list(map(lambda x: Decimal(x), coeffs))
    return coeffs

def getValidDegree():
    while True:
        len_coeffs = input("What degree is your polynomial (whole number ≥ 0)?\n").strip()
        # Given the input, perform some checks
        # If any of the if or elif statements return true, the else statement won't trigger, returning to the start of the loop and asking for another input.

        # First, check if the input is actually valid as a number.
        try:
            len_coeffs = float(len_coeffs)
        except:
            print("That's not a number.\n")
            continue
        # Check if it's within the bounds of the possibilities of the degree of a polynomial.
        if not(0 <= len_coeffs < inf):
            print("Degree must be 0 ≤ n < ∞.")
        # Check that the degree is a whole number by checking if it is equal to its integer counterpart.
        elif not(len_coeffs == int(len_coeffs)):
            print("That's not a whole number.")
            
        # If the input passed all conditions, exit the while loop and begin the inputs for the polynomial terms
        else:
            len_coeffs = int(len_coeffs)
            break
        print()
    print("\nIf you make a mistake, type 'r' to restart.\n")
    return len_coeffs

def getValidCoeffs(len_coeffs):
    coefficients = []
    for i in range(len_coeffs, -1, -1):
        while True:
            coeff = input(f"What is the degree {i} term ({mkTerm(1, i)})?\t").strip().lower()
            if coeff == "r":
                print("-"*10)
                return getValidCoeffs(getValidDegree())
            try:
                coeff = float(coeff)
            except:
                print("Not a number.")
                continue
            coefficients.insert(0, int(coeff) if coeff % 1 == 0 else float(coeff))
            break
    print()
    return coefficients

def getinputs():
    return getValidCoeffs(getValidDegree())

def calculate(coeffs, x):
    out = 0
    x = Decimal(x)
    for index, i in enumerate(list(map(lambda x: Decimal(x), coeffs))): 
        try:
            out += i * (x ** index)
        except:
             out += i
    return out

def maxRangeOfRoots(coeffs):
    nums=[0]
    for i in range(len(coeffs)-1):
        nums.append((abs(coeffs[i]/(coeffs[-1]) if i != 0 else (2*coeffs[-1]))) ** (Decimal(1/(len(coeffs)-i-1))))
    return 2 * max(nums)

def polyDivide(dividend, divisor):
    # Initialize the quotient and remainder
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    remainder = dividend.copy()

    # Perform polynomial division
    for i in range(len(dividend) - len(divisor), -1, -1):
        # Compute the current quotient term
        quotient[i] = remainder[i + len(divisor) - 1] / divisor[-1]

        # Eliminate the current term and update the remainder
        for j in range(len(divisor)):
            remainder[i + j] -= quotient[i] * divisor[j]

    # Since we're only ever dividing by a root, the remainder is negligible.
    return quotient


def getDerivative(coeffs):
    # Uses power rule to calculate the derivative of a function
    # d/dx (x**n) = nx**(n-1)
    derivative = []
    for degree in range(len(coeffs)):
        derivative.append(degree * coeffs[degree])
    derivative.pop(0) # delete what used to be the constant
    return derivative
    
def newtonsMethod(tolerance, initialGuess, coeffs):
    '''
    An intelligent method of performing a guess-and-check. Follows the formula:

    x_(n+1) = x_n - (f(x_n)/f'(x_n))

    where f(x) is the given function, f'(x) is its derivative, n is any step number and n+1 is the next step.
    '''
    guess = Decimal(initialGuess) # uses some arbitrary number to create a starting guess
    derivative_coeffs = getDerivative(coeffs)
    i = 0
    maxIterations = range(250) # if it diverges away from our zero, we don't want it to go on for forever
    for _ in maxIterations:
        numerator = calculate(coeffs, guess) 
        denominator = calculate(derivative_coeffs, guess)
        if denominator == 0: # if we're not dividing by zero
            return None
        else: # if we are trying to divide by zero, we found a locally flat part.
            guess -= (numerator / denominator)
        if abs(calculate(coeffs, guess)) < tolerance: # if we're within our tolerance of accuracy to zero, consider the answer to be correct
            return guess # and return it
        i += 1
    return None

def zeros(coeffs, tolerance, out=None):
    if out is None:
        out = set()
    try:
        allnumbers = list(map(lambda x: int(x), coeffs))
    except:
        return out

    coeffs = trimcoeffs(coeffs)
        
    if len(coeffs) ==  1: # degree 0 polynomial
        if coeffs[0] == 0:
            out.add(float('inf'))

    elif len(coeffs) == 2: # degree 1 polynomial; use general equation
        out.add(round(-coeffs[0] / coeffs[1], 4))

    elif len(coeffs) == 3: # degree 2 polynomial; use quadratic solution
        a = Decimal(coeffs[2])
        b = Decimal(coeffs[1])
        c = Decimal(coeffs[0])
        discriminator = (b**2) - (4 * a * c)
        if discriminator >= 0:
            num = Decimal(sqrt(discriminator))
            b /= -2 * a
            num /= 2 * a
            out.add(round(b - num, 4))
            out.add(round(b + num, 4))
        
    elif len(coeffs) > 3: # works for any n-degree polynomial; use Newton's method of approximation
        maxRange = maxRangeOfRoots(coeffs) # range of guesses
        guesses = [-maxRange, maxRange, 0]
        for i in guesses:
            zero = newtonsMethod(tolerance, i, coeffs)
            if zero is not None:
                coeffs = polyDivide(coeffs, [-zero, 1])
                zero = float(round(zero, 4)) + 0.0
                didWeAdd = len(out)
                out.add(zero) # add it to our list
                didWeAdd = len(out) - didWeAdd
                if didWeAdd:
                    zeros(coeffs, tolerance, out)
                break

    out = list(out)
    for i in range(len(out)):
        if out[i]//1 == out[i]:
            out[i]=int(out[i])
    return sorted(list(set(out)))

def main():
    while True:
        tolerance = 1e-15

        coeffs = getinputs()
        # coeffs = [-6, 3, -6, 12, -4, 7, -7, 1, 0, 5, -2, -4, -12, 2, 7, 12, -7, -10, -4, 3, 9, -7, 0, -8, 14, -3, 9, 2, -3, -10, -2, -6, 1, 10, -3, 1, 7, -7, 7, -12, -5, 8, 6, 10, -8, -8, -7, -3, 9, 1, 6, 6, -2, -3, -10, -2, 3, 5, 2, -1, -1, -1, -1, -1, 1, 2, 2, -1, -2, -1, 0, 1]
        coeffs = trimcoeffs(coeffs)

        print(f"Input equation: f(x) = {formatPoly(coeffs)}\n")

        startTime = time()
        zero = zeros(coeffs, tolerance)
        timeTaken = time() - startTime

        print(f"""{(", ".join(str(i) for i in zero)) + (" is " if len(zero) == 1 else " are ") + ("the location of the zero" + ('es' if len(zero) != 1 else '') + " " + "(" + str(len(zero)) + ")") if len(zero) > 0 else "No zeroes found"}. Took {timeTaken} seconds.""")
        while True:
            again = input("\nWant to find more roots? (y/n)\t").lower().strip()
            if again == "y" or again == "yes":
                print()
                break
            elif again == "n" or again == "no":
                return
            else:
                print("Didn't understand.")
main()
