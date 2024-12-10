from time import perf_counter_ns as time
import re

def isPrime(x: int) -> bool:
    return not re.match(r'^.?$|^(..+?)\1+$', '1'*x)

    return True
def isPrime3(n):
    if n < 2:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            print(i, n//i)
            return False
        i += 1
    return True

def test_time(func, *args, **kwargs):
    iters = kwargs.pop('iters', 100) # defaults to 100 iters if not given
    timetaken = 0
    for i in range(iters):
        beg = time()
        result = func(*args, **kwargs)
        end = time()
        timetaken += end-beg
    print(result)
    return (timetaken/iters) / 1e9

n = 147_573_952_589_676_412_927

# avg_time = test_time(isPrime, 15487457, iters=1)
avg_time3 = test_time(isPrime3, n, iters=1)
# print(avg_time)
print(avg_time3)

##for i in range(100):
##    print(i, isPrime2(i))
