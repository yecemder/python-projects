from timeit import default_timer as time

def more_than_zero(number):
    return number > 0


testList1 = [i for i in range(-5, 15)]
testList2 = [i for i in range(-500, 1500)]
testList3 = [i for i in range(-50000, 150000)]
testList4 = [i for i in range(-5000000, 15000000)]


def test_times(List):
    startTimeAny = time()
    moreThanZeroAny = any(map(more_than_zero, List))
    timeTakenAny = time() - startTimeAny

    moreThanZeroFor = False
    startTimeFor = time()
    for i in List:
        if more_than_zero(i):
            moreThanZeroFor = True
            break
    timeTakenFor = time() - startTimeFor
    return timeTakenAny, timeTakenFor

forVsAnd1 = test_times(testList1)
forVsAnd2 = test_times(testList2)
forVsAnd3 = test_times(testList3)
forVsAnd4 = test_times(testList4)

print(forVsAnd1)
print(forVsAnd2)
print(forVsAnd3)
print(forVsAnd4)
