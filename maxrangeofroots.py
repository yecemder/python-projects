from random import randint, uniform
import numpy as np

def Lagrange(coeffs):
    nume = 0
    for i in range(len(coeffs)-1):
        nume += abs(coeffs[i])
    return max(1, nume/abs(coeffs[-1]))

def Cauchy(coeffs):
    nums=[]
    for i in range(len(coeffs)-1):
        nums.append(abs(coeffs[i]/(coeffs[-1] if i != 0 else 2*coeffs[-1])) ** (1/(len(coeffs)-i-1)))
    return 2 * max(nums)

def CauchyOG(coeffs):
    nums=[0]
    for i in range(len(coeffs)-1):
        nums.append(abs(coeffs[i]/coeffs[-1]))
    return 2 * max(nums)

def Fujiwara(coeffs):
    nums = []
    denom = coeffs[-1]
    for i in range(len(coeffs)-2, -1, -1):
        if i == 0:
            denom *= 2
        num = abs(coeffs[i]/denom)**(1/(len(coeffs)-i-1))
        nums.append(num)

    return 2*max(nums)

coeffs = [9,9,43,-2,-4,1,-7]
def genList():
    global coeffList
    coeffList = []
    length = randint(4, 20)
    for i in range(length):
        coeffList.append(round(uniform(-10, 10), 4))
    print(coeffList)
    print("degree", length-1)

def roots(coeffs):
    coeffL = coeffs
    coeffL.reverse()
    coeffL = np.array(coeffL)
    roots_np = np.roots(coeffL)
    roots = roots_np.tolist()
    roots.reverse()
    out = []
    for i in range(len(roots)):
        if roots[i].imag == 0:
            out.append(roots[i].real)
    return out
    
    

genList()

print("Cauchy predicts", Cauchy(coeffList))

print("Cauchy Original predicts", CauchyOG(coeffList))

print("Lagrange predicts", Lagrange(coeffList))

print("Fujiwara predicts", Fujiwara(coeffList))



print("\nReal roots:", roots(coeffList))
