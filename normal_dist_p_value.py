from math import pi, sqrt, e, inf

# integration of normal distribution from lower bound (LBound)
# to upper bound (UBound)

def sgn(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def erf(x):
    # Error function - part of the integral of the normal distribution,
    # no clue why. Uses a Burmann's Theory series to approximate value.
    # True error function: erf(x) = 2/sqrt(pi) * integrate 0, x (e**-(t**2)) dt
    
    first = 2/sqrt(pi) * sgn(x)
    second = sqrt(1-(e ** -(x**2)))
    third = sqrt(pi)/2 + (31/200 * (e**-(x**2))) - (341/8000 * (e**-(2*(x**2))))
    return first * second * third


def p_value(LBound=-inf, UBound=inf, mu=0, sigma=1, inside=True):
    # indefinite integral of normal distribution is
    # -1/2 * erf((mu-x) / (sqrt(2) * sigma))
    # Inside True means we want the value inside the bounds,
    # whereas false means the value outside.
    
    
    lower_bound = -1/2 * erf((mu - LBound) / (sqrt(2) * sigma))
    
    upper_bound = -1/2 * erf((mu - UBound) / (sqrt(2) * sigma))

    if inside:
        return upper_bound - lower_bound
    return 1 - (upper_bound - lower_bound)

print(p_value(1))

