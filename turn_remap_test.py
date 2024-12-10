from math import sin, pi
turnNL = 3
def remap(iturn):
    if iturn == 0:
        return 0
    denominator = sin(pi / 2 * turnNL)
    firstRemap = sin(pi / 2 * iturn) / denominator
    return sin(pi / 2 * turnNL * firstRemap) / denominator

for i in range(-30, 30+1, 1):
    print(f"remap {i}: {remap(i)}")
