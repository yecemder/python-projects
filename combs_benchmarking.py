# combs benchmarking
from timeit import default_timer as time

def combs_recursive(a):
    if len(a) == 0:
        return [[]]
    cs = []
    for c in combs_recursive(a[1:]):
        cs += [c, c+[a[0]]]
    return cs

def combs_iterative(a):
    result = [[]]
    for item in a:
        new_combinations = [current + [item] for current in result]
        result.extend(new_combinations)
    return result

def testfunc(func, iters, inputs):
    beg = time()
    for i in iters:
        func(inputs)
    end = time()
    return end-beg

cr = combs_recursive
ci = combs_iterative

iters = range(10)
testlist = list(range(20))

# time_r = testfunc(cr, iters, testlist)
time_i = testfunc(ci, iters, testlist)

# print(f"recursive: {time_r}")
print(f"iterative: {time_i}")
