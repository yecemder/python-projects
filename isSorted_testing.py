import timeit
from numba import njit

@njit
def isSorted_numba(array):
    for i in range(1, len(array)):
        if array[i] < array[i - 1]:
            return False
    return True

def isSorted_while(array):
    i = 1
    while i < len(array):
        if array[i] < array[i - 1]:
            return False
        i += 1
    return True

def isSorted_genexpr(array):
    return all(array[i] <= array[i+1] for i in range(len(array)-1))

def isSorted_zip(array):
    for prev, curr in zip(array, array[1:]):
        if curr < prev:
            return False
    return True

# Test with a sorted array and a large unsorted array
test_array_sorted = list(range(1000000))
test_array_unsorted = list(range(1000000, 0, -1))

# Warm up Numba to account for compilation time
isSorted_numba(test_array_sorted)
isSorted_numba(test_array_unsorted)

# Measure performance
def measure_time(func, array):
    start = timeit.default_timer()
    result = func(array)
    end = timeit.default_timer()
    return end - start, result

print("Timing with sorted array:")
print("While loop sorted:", *measure_time(isSorted_while, test_array_sorted))
print("Generator expression sorted:", *measure_time(isSorted_genexpr, test_array_sorted))
print("Zip version sorted:", *measure_time(isSorted_zip, test_array_sorted))
print("Numba version sorted:", *measure_time(isSorted_numba, test_array_sorted))

print("\nTiming with unsorted array:")
print("While loop unsorted:", *measure_time(isSorted_while, test_array_unsorted))
print("Generator expression unsorted:", *measure_time(isSorted_genexpr, test_array_unsorted))
print("Zip version unsorted:", *measure_time(isSorted_zip, test_array_unsorted))
print("Numba version unsorted:", *measure_time(isSorted_numba, test_array_unsorted))
