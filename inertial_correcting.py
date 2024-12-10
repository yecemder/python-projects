from math import pi, sqrt, e, inf, cos, sin, atan
from timeit import default_timer as time

def sgn(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def mean(values):
    n = 0
    for i in values:
        n += i
    return n/len(values)

def SD(values):
    mu = mean(values)
    n = 0
    for i in values:
        n += (i-mu)**2
    return sqrt(n/len(values))

def erf(x):
    # Error function - part of the integral of the normal distribution,
    # Uses a Burmann's Theory series to approximate value.
    # True error function: erf(x) = 2/sqrt(pi) * integrate 0, x (e**-(t**2)) dt
    
    first = 2/sqrt(pi) * sgn(x)
    second = sqrt(1-(e**-(x**2)))
    third = sqrt(pi)/2 + (31/200 * (e**-(x**2))) - (341/8000 * (e**-(2*(x**2))))
    
    return first * second * third


def p_value(LBound=-inf, UBound=inf, m=0, s=1, inside=True):
    # indefinite integral of normal distribution is
    # -1/2 * erf((mu-x) / (sqrt(2) * sigma))
    # Inside True means we want the value inside the bounds,
    # whereas false means the value outside.
    
    lower_bound = -1/2 * erf((m - LBound) / (sqrt(2) * s))

    upper_bound = -1/2 * erf((m - UBound) / (sqrt(2) * s))
    
    if inside:
        return upper_bound - lower_bound
    return 1 - (upper_bound - lower_bound)

def softmax(values, temperature):
    raised = [(e**(i/temperature)) for i in values]
    summed = sum(raised)
    adjusted = [i/summed for i in raised]
    return adjusted


def adjusted_heading(inputs, temperature=0.01):
    # Check if the user specified that the input is in radians.
    # If not, convert to radians - we'd prefer doing the math in radians 
    # or even revolutions because at some point we raise e to the power of each value and that gets
    # very big, very quick with bigger numbers, and Python's trig functions work in radians.
    
    inputs = [(i * 2 * pi / 360) for i in inputs]
        
    mu = mean(inputs) # Get mean of set
    sigma = SD(inputs) # Get standard deviation of set
    
    if sigma == 0: # if the set of numbers are all equal, just skip the math and return the first input
        return (inputs[0] * 360 / (2 * pi))
    
    p_values = [] # Create list of P values
    for angle in inputs:
        if sigma != 0:
            # If the input value is less than mu, use input as upper bound
            if angle < mu:
                p_values.append(p_value(UBound=angle, m=mu, s=sigma))
            # otherwise use it as the lower
            else:
                p_values.append(p_value(LBound=angle, m=mu, s=sigma))
        else:
            p_values.append(1)

    # From P values, get magnitude of vectors
    magnitudes = softmax(p_values, temperature)

    # Use magnitudes as weight in a weighted average of the angles to preserve net rotation information
    weighted_heading = sum([(magnitudes[i] * inputs[i]) for i in range(len(inputs))])

    
    # Get vector components of the sum of vectors with softmax as the magnitudes
    adjusted_x = sum([(magnitudes[i] * cos(inputs[i])) for i in range(len(inputs))])
    adjusted_y = sum([(magnitudes[i] * sin(inputs[i])) for i in range(len(inputs))])

    # Get angle of vector
    adjusted_theta = atan(adjusted_y/adjusted_x)

    # Move vector to within 180 degrees of the weighted average
    while abs(adjusted_theta - weighted_heading) > pi: # While we're more than half a rotation off
        # Move the angle positive if it's too low
        if adjusted_theta - weighted_heading < 0:
            adjusted_theta += 2 * pi
        # Negatively if it's too high
        else:
            adjusted_theta -= 2 * pi
    
    return (adjusted_theta * 360 / (2 * pi))
    
    # return magnitudes

inputs = [15, 17, 25]

starttime = time()
heading_out=adjusted_heading(inputs)
timetaken = time()-starttime
print(f"took {timetaken} seconds to finish")
print(f"inputs: {inputs}")
print(f"output: {heading_out}")





