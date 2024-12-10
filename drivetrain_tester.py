#drivetrain testing

def test(testdict, algorithm):
    for i in testdict:
        print(f"in: {i[0]}, {i[1]} \ntypical: {i[0] + i[1]}, {i[0] - i[1]} \nadjusted: {algorithm(i[0], i[1])}\n")

def alg(inL, inR):
    
    inL, inR = inL/100, inR/100
    leftSpeed = inL + (abs(inL) * inR)
    rightSpeed = inL - (abs(inL) * inR)
    if rightSpeed > 1:
        leftSpeed = 0 if leftSpeed == 0 else rightSpeed / leftSpeed
    if leftSpeed > 1:
        rightSpeed = 0 if rightSpeed == 0 else leftSpeed/rightSpeed
    leftSpeed, rightSpeed = leftSpeed * 100, rightSpeed * 100
    return leftSpeed, rightSpeed

def sign(num):
    if num >= 0:
        return 1
    if num < 0:
        return -1
    return None
    

def alg2(inL, inR):
    speedCap = 100 # positive integer, should be 100 unless otherwise needed

    # Typical basic arcade code
    leftSpeed = inL + inR
    rightSpeed = inL - inR
    
    # if either motor speed isn't within the bounds of -speedCap to speedCap,
    # use proportional clamping to bring both speeds to within speedCap
    # by finding the factor that brings down the offending motor to speedCap
    # and dividing the other motor's speed by same factor
    # also uses elif to skip an unnecessary step for the boolean logic checks
    if not -speedCap < leftSpeed < speedCap:
        speedFactor = leftSpeed / (speedCap * sign(leftSpeed))
        leftSpeed = 100 * sign(leftSpeed)
        rightSpeed = rightSpeed / speedFactor
        
    elif not -speedCap < rightSpeed < speedCap:
        speedFactor = rightSpeed / (speedCap * sign(rightSpeed))
        leftSpeed = leftSpeed / speedFactor
        rightSpeed = 100 * sign(rightSpeed) # might be slower to call another function... needs testing
    
    return leftSpeed, rightSpeed

    

testcases = [[100, -100], [100, -80], [100, -60], [100, -40], [100, -20], [100, 0], [100, 20], [100, 40], [100, 60], [100, 80], [100, 100], [80, -100], [80, -80], [80, -60], [80, -40], [80, -20], [80, 0], [80, 20], [80, 40], [80, 60], [80, 80], [80, 100], [60, -100], [60, -80], [60, -60], [60, -40], [60, -20], [60, 0], [60, 20], [60, 40], [60, 60], [60, 80], [60, 100], [40, -100], [40, -80], [40, -60], [40, -40], [40, -20], [40, 0], [40, 20], [40, 40], [40, 60], [40, 80], [40, 100], [20, -100], [20, -80], [20, -60], [20, -40], [20, -20], [20, 0], [20, 20], [20, 40], [20, 60], [20, 80], [20, 100], [0, -100], [0, -80], [0, -60], [0, -40], [0, -20], [0, 0], [0, 20], [0, 40], [0, 60], [0, 80], [0, 100], [-20, -100], [-20, -80], [-20, -60], [-20, -40], [-20, -20], [-20, 0], [-20, 20], [-20, 40], [-20, 60], [-20, 80], [-20, 100], [-40, -100], [-40, -80], [-40, -60], [-40, -40], [-40, -20], [-40, 0], [-40, 20], [-40, 40], [-40, 60], [-40, 80], [-40, 100], [-60, -100], [-60, -80], [-60, -60], [-60, -40], [-60, -20], [-60, 0], [-60, 20], [-60, 40], [-60, 60], [-60, 80], [-60, 100], [-80, -100], [-80, -80], [-80, -60], [-80, -40], [-80, -20], [-80, 0], [-80, 20], [-80, 40], [-80, 60], [-80, 80], [-80, 100], [-100, -100], [-100, -80], [-100, -60], [-100, -40], [-100, -20], [-100, 0], [-100, 20], [-100, 40], [-100, 60], [-100, 80], [-100, 100]]
    
test(testcases, alg2)
