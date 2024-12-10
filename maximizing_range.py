from math import tan, pi

vi = 10
h = -3

ranges = []

def degToRad(angle):
    return angle*pi/180

for angle in range(91):
    ranges.append(h*tan(degToRad(angle))/vi)

for i in range(len(ranges)):
    print(i, ranges[i])
