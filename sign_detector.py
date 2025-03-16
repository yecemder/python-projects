from math import inf, copysign
from time import perf_counter_ns as time

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

def sign_ternary(x):
    return 1 if x>0 else -1 if x<0 else 0

def mathsign(x):
    return copysign(1, x)
    
num = 13
reps = 10000000

st5 = time()
for i in range(reps):
    n = sign_ternary(num)
nd5 = time()
t5 = nd5-st5

st1 = time()
for i in range(reps):
    j = sign(num)
nd1 = time()
t1 = nd1 - st1

st2 = time()
for i in range(reps):
    k = sigmoid_sign(num)
nd2 = time()
t2 = nd2 - st2

st3 = time()
for i in range(reps):
    l = div_sign(num)
nd3 = time()
t3 = nd3 - st3

st4 = time()
for i in range(reps):
    m = mathsign(num)
nd4 = time()
t4 = nd4-st4

print(f"piecewise sign took {t1/1e9} seconds")
print(f"sigmoid sign took {t2/1e9} seconds")
print(f"div sign took {t3/1e9} seconds")
print(f"copysign took {t4/1e9} seconds")
print(f"ternary took {t5/1e9} seconds")

