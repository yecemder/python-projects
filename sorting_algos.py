from time import perf_counter_ns as time
import random

def mergeSort(arr):
    lenarr = len(arr)
    if lenarr < 2: return arr
    return mergeCombine(mergeSort(arr[0:lenarr//2]),
                        mergeSort(arr[lenarr//2:lenarr]))

def mergeCombine(list1, list2):
    len1 = len(list1)
    len2 = len(list2)
    out = []
    index1, index2 = 0, 0
    for _ in range(len1+len2):
        if (index1 >= len1):
            out.append(list2[index2])
            index2 += 1
        elif (index2 >= len2):
            out.append(list1[index1])
            index1 += 1
        elif (list1[index1] < list2[index2]):
            out.append(list1[index1])
            index1 += 1
        else:
            out.append(list2[index2])
            index2 += 1
    return out

def generateArray(length):
    bound = int(1.5*pow(length, 1.05))
    return [random.randint(0, bound) for _ in range(length)]

def verifySort(arr):
    for i in range(len(arr)-1):
        if arr[i] > arr[i+1]:
            print("found false at", i, arr[i], arr[i+1])
            return False

    return True

def test_time(func, *args, **kwargs):
    iters = kwargs.pop('iters', 100) # defaults to 100 iters if not given
    timetaken = 0
    for i in range(iters):
        beg = time()
        result = func(*args, **kwargs)
        end = time()
        timetaken += end-beg
    return (timetaken/iters) / 1e9

def main():
    length = 1_000_000
    arr = generateArray(length)
    time = test_time(mergeSort, arr, iters = 10)
    print(time)

if __name__ == "__main__":
    main()