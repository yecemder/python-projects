from math import sqrt
from numpy import prod
from timeit import default_timer as time

def P(a, b):
    out = 1
    for j in range(a, b):
        out *= -(6*j - 1)*(2*j - 1)*(6*j-5)
    return out

def Q(a, b):
    result = 1
    for j in range(a, b):
        result *= 10939058850032000 * (j ** 3)
    return result
    #return prod((10939058850032000 * (j ** 3) for j in range(a,b))

def S(a, b):
    return sum((P(a, k+1)/Q(a, k+1)) * (545140134*k+13591409) for k in range(a, b))

def R(a, b):
    return Q(a, b) * S(a, b)

def compute(n):
    return (426880*sqrt(10005) * Q(1, n))/(13591409*Q(1, n) + R(1, n))

beg = time()
for i in range(10):
    comp = compute(10)
end = time()

print(comp)
print(f"{end-beg} seconds taken.")
