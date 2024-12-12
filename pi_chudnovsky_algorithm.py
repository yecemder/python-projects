#Note: For extreme calculations, other code can be used to run on a GPU, which is much faster than this.
import decimal


def binary_split(a, b):
    if b == a + 1:
        Pab = -(6*a - 5)*(2*a - 1)*(6*a - 1)
        Qab = 10939058860032000 * a**3
        Rab = Pab * (545140134*a + 13591409)
    else:
        m = (a + b) // 2
        Pam, Qam, Ram = binary_split(a, m)
        Pmb, Qmb, Rmb = binary_split(m, b)
        
        Pab = Pam * Pmb
        Qab = Qam * Qmb
        Rab = Qmb * Ram + Pam * Rmb
    return Pab, Qab, Rab


def chudnovsky(n):
    """Chudnovsky algorithm."""
    P1n, Q1n, R1n = binary_split(1, n)
    return (426880 * decimal.Decimal(10005).sqrt() * Q1n) / (13591409*Q1n + R1n)

def bbp(n):
    total = decimal.Decimal(0)
    for k in range(n):
        kd = decimal.Decimal(k)
        total += (1/(16**kd) * (4/(8*kd+1) - 2/(8*kd+4) - 1/(8*kd+5) - 1/(8*kd+6)))
    return total

print(f"1 = {chudnovsky(2)}")  # 3.141592653589793238462643384

decimal.getcontext().prec = 10000 # number of digits of decimal precision
for n in range(2,1000+1):
    #print(f"{n} = {chudnovsky(n)}")  # 3.14159265358979323846264338...
    pass

##print(chudnovsky(10000))
##print(chudnovsky(10001))

print(bbp(100))
