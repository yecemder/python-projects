from math import inf, copysign
from timeit import default_timer as time

def sigmoid_sign(x):
    return 2/(1 + inf**-x) - 1

def div_sign(x):
    return x/abs(x)

def sign(x):
    if x > 0:
        return 1.0
    if x < 0:
        return -1.0
    return 0.0

def mathsign(x):
    return copysign(1, x)
    
num = 13
reps = 10000000

startTime = time()
for i in range(reps):
    j = sign(num)
endTime1 = time()-startTime

startTime = time()
for i in range(reps):
    k = sigmoid_sign(num)
endTime2 = time()-startTime

startTime = time()
for i in range(reps):
    l = div_sign(num)
endTime3 = time()-startTime

startTime = time()
for i in range(reps):
    m = mathsign(num)
endTime4 = time()-startTime

print(f"piecewise sign took {endTime1} seconds")
print(f"sigmoid sign took {endTime2} seconds")
print(f"div sign took {endTime3} seconds")
print(f"copysign took {endTime4} seconds")

