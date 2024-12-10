from math import sqrt, inf
from numpy.polynomial import polynomial as P
from numpy.polynomial import polyutils as pu
from timeit import default_timer as time
from decimal import Decimal
from decimal import getcontext

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
    out = ""
    outList = []
    try:
        ints = list(map(lambda x: int(x), coeffs))
    except:
        return f"Input issue - couldn't create an expression from input expression {coeffs}"
    if coeffs == [0]:
        return "0"
    for i in range(len(coeffs)): # create terms
        if coeffs[i] < 0:
            t = mkTerm(coeffs[i], i)
            if t is not None:
                outList.append("-" + t)
        else:
            t = mkTerm(coeffs[i], i)
            if t is not None:
                outList.append(t)
                
    outList.reverse()
    for i in range(len(outList)): # append them together
        if outList[i] is not None:
            out += str(outList[i])
            if i < len(outList) - 1:
                out += " + "

    out = list(out)
    for i in range(len(out)): # clean signs
        if out[i] == "+" and out[i+1] == " " and out[i+2] == "-":
            out[i] = "-"
            out[i+2] = ""
            
    return "".join(out)

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
            print("Can't use a degree that's less than zero or greater than infinity.")

        # Check that the degree is a whole number by assigning a variable to its integer representation, subtracting the two,
        elif not(len_coeffs == int(len_coeffs)):
            print("That's not a whole number.")
        # If the input passed all conditions, exit the while loop and begin the inputs for the polynomial terms
        else:
            len_coeffs = int(len_coeffs)
            break
    return len_coeffs

def getValidCoeffs(len_coeffs):
    coefficients = []
    for i in range(len_coeffs, -1, -1):
        while True:
            coeff = input(f"What is the degree {i} term ({mkTerm(1, i)})? ").strip()
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

def calculateAll(coeffs, values):
    out = []
    for v in values:
        out += [(v,calculate(coeffs,v))]
    return out

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
        nums.append((abs(coeffs[i]/(coeffs[-1]) if i != 0 else (2*coeffs[-1]))) ** (1/(len(coeffs)-i-1)))
    return 2 * max(nums)

def polyDivide(c1, c2):
    print(c1)
    print(c2)
    # c1, c2 are trimmed copies
    [c1, c2] = pu.as_series([c1, c2])
    # NOTE: MAP AS DECIMALS
    if c2[-1] == 0:
        raise ZeroDivisionError()

    lc1 = len(c1)
    lc2 = len(c2)
    if lc1 < lc2:
        return c1[:1]*0, c1
    elif lc2 == 1:
        return c1/c2[-1], c1[:1]*0
    else:
        dlen = lc1 - lc2
        scl = c2[-1]
        c2 = c2[:-1]/scl
        i = dlen
        j = lc1 - 1
        while i >= 0:
            print(c1[j])
            c1[i:j] -= c2*c1[j]
            i -= 1
            j -= 1
        return c1[j+1:]/scl, pu.trimseq(c1[:j+1])

def getDerivative(coeffs):
    # Uses power rule to calculate the derivative of a function
    # d/dx (x**n) = nx**(n-1)
    derivative = []
    for degree in range(len(coeffs)):
        derivative.append(degree * coeffs[degree])
    derivative.pop(0)
    return derivative
    
def newtonsMethod(tolerance, initialGuess, coeffs):
    '''
    An intelligent method of performing a guess-and-check. Follows the formula:

    x_(n+1) = x_n - (f(x_n)/f'(x_n))

    where f(x) is the given function, f'(x) is its derivative, n is any step number and n+1 is the next step.
    '''
    guess = Decimal(initialGuess) # uses some arbitrary number to create a starting guess
    derivative_coeffs = getDerivative(coeffs)
    f_xn = lambda coef, x: calculate(coeffs, x)
    fprime_xn = lambda derivative, x: calculate(derivative, x) # same thing but it returns f'(x)
    i = 0
    maxIterations = 500 # if it diverges away from our zero, we don't want it to go on for forever
    while i < maxIterations:
        numerator = f_xn(coeffs, guess) # creates f(x_n)
        denominator = fprime_xn(derivative_coeffs, guess) # creates f'(x_n)
        if denominator != 0: # if we're not dividing by zero
            guess -= (numerator / denominator)
        else: # if we are trying to divide by zero, we found a locally flat part.
            return None
        if abs(calculate(coeffs, guess)) < tolerance: # if we're within our tolerance of accuracy to zero, consider the answer to be correct
            return guess # and return it
        i += 1
    return None
    
def zeros(coeffs, out=None):
    if out is None:
        out = set()
    try:
        allnumbers = list(map(lambda x: int(x), coeffs))
    except:
        return out

    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop(-1)
    
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
        guesses = [-maxRange, maxRange, 1, -1]
        for i in guesses:
            zero = newtonsMethod(tolerance, i, coeffs)
            if zero is not None:
                coeffs = polyDivide(coeffs, [-zero, 1])
                zero = round(zero, 4)      
                if zero == 0:
                    zero = abs(zero) # ensure that we don't give "-0.0" as an answer just because it looks better
                didWeAdd = len(out)
                out.add(zero) # add it to our list
                didWeAdd = len(out) - didWeAdd
                if didWeAdd:
                    zeros(coeffs, out)
                break

    out = list(out)
    for i in range(len(out)):
        if out[i]%1 == 0:
            out[i]=int(out[i])
    return sorted(list(set(out)))

tolerance = 1e-20

# coeffs = [-531105942986.0825, 4382409875.638045, -36161365.85064894, 298384.7247050617, -2462.123784790039, 20.31543424151158, -0.23945184266411346, 0.11610713829328567, -0.07097753917540572, -0.10633582324166824, 0.16352802206454076, -0.04313113710108851, 0.13987153717105016, -0.14519709820481985, 0.07917692175353963]

coeffs = [-10.904, 8.9947, -9.7651, -19.3222, -8.521, -10.1664, -1.1505, -16.8317, 4.1998, 19.3148, -17.1664, -6.7644, -6.5662, 4.7922, 13.1734, 0.9356, 6.7483]

coeffs = [-1, -1, 1]

# Alternatively, use this "getinputs()" function for command-line usability
# coeffs = getinputs()

print(f"Input equation: f(x) = {formatPoly(coeffs)}\n")

startTime = time()
zero = zeros(coeffs)
timeTaken = time() - startTime

print(f"""{(", ".join(str(i) for i in zero)) + (" is " if len(zero) == 1 else " are ") + ("the location of the zero" + ('es' if len(zero) != 1 else '') + " " + "(" + str(len(zero)) + ")") if len(zero) > 0 else "No zeroes found"}. Took {timeTaken} seconds.""")
