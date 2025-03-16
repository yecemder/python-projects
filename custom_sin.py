from math import sin
from math import pi, fmod, factorial, floor

def sgn(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def clamp(x, mi, ma):
    return min(max(x, mi), ma)

def cmod(a, n):
    return a - (n * floor(a/n))

def interp(a, b, t):
    return b * t + a * (1-t)

def custom_sin(x):
    # Calculate sign of final output
    # sign = sgn((x-pi)%(2*pi) - pi)
    sign = sgn(cmod((x-pi),(2*pi)) - pi)

    # Clean input to 0 ≤ x ≤ π/2
    # x %= pi
    x = cmod(x, pi)  # Trim x to [0, π)
    x = pi - x if x > pi/2 else x  # Reflect about x=π/2 if x is on right side
    # print("reduced x:", x)
    
    # Taylor series of sinx
    out = 0
    terms = 11  # Hard max number of terms that can be used
    prev = 0
    for n in range(terms+1):
        out += (-1 if n & 1 else 1) * (x ** (2*n + 1)) / (factorial(2*n + 1))
        if out - prev == 0:
            break
        prev = out
    return clamp(out, 0, 1) * sign

num_of_samples = 200
testrange_min = -100 * pi
testrange_max = 100 * pi
zeros = 0
for i in range(num_of_samples):
    point = interp(testrange_min, testrange_max, i/num_of_samples)
    print("p:", point, "c:", custom_sin(point), "s:", sin(point))
    if custom_sin(point) == 0:
        zeros += 1

print("Zeroes:", zeros)