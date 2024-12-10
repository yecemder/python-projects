def sign(num):
    if num >= 0:
        return 1
    if num < 0:
        return -1
    return None

def PIDcompute(PV, SP, Kp, Ki, Kd, starti, settleTime, settleRange, tick):
    global accumulatedError, prevError, timeSettled, timeSettled

    err = SP - PV

    if abs(err) < starti:
        accumulatedError += err
    if (err > 0 and prevError < 0) or (err < 0 and prevError > 0):
        accumulatedError = 0

    p = Kp * err
    i = Ki * accumulatedError
    d = Kd * (err - prevError)
    change = p + i + d
    prevError = err

    return change

def inSettlingRange(PV, SP, settleRange):
    return -settleRange + SP < PV < settleRange + SP

def PID(PV, SP, Kp, Ki, Kd, starti, settleTime, settleRange, tick, timeout, maxMotorRPM):
    global prevError, accumulatedError, timeSettled

    prevError = SP - PV
    accumulatedError = 0
    timeElapsed = 0
    timeSettled = 0
    maxDegreesPerTick = tick * (maxMotorRPM / 60) * 360 # Max degrees per tick a motor can spin
    while True:
        if timeElapsed >= timeout:
            print(f"timeout after {round(timeElapsed/tick)} ticks ({round(timeElapsed, 2)} seconds over {tick} second ticks)")
            return
        pid = PIDcompute(PV, SP, Kp, Ki, Kd, starti, settleTime, settleRange, tick)
        timeElapsed += tick
        PV = hypotheticalMotor(maxDegreesPerTick, pidToMotor(pid, maxDegreesPerTick), PV, tick)
        if inSettlingRange(PV, SP, settleRange):
            timeSettled += tick
        else:
            timeSettled = 0
        if timeSettled >= settleTime:
            print(f"final motor position: {PV} degrees\n")
            print(f"settled in {round(timeElapsed/tick)} ticks ({round(timeElapsed, 2)} seconds with ticks at {tick} second intervals)\ntolerance: +-{settleRange} degrees, time tolerance: {settleTime}")
            return
        print(f"motor's degrees spun: {PV}\n")
        # add a delay based on tick here?

def pidToMotor(pid, maxPerTick):  
    # Input: Number of degrees we want to motor to turn in this tick, max number of degrees we CAN turn in one tick
    # Output: a motor velocity in percentage (-100 <= x <= 100)
    return (pid / maxPerTick) * 100.0 if -maxPerTick <= pid <= maxPerTick else sign(pid) * 100.0
    
def hypotheticalMotor(maxDegreesPerTick, spinSpeed, position, tick):
    # Inputs: parameters of a motor  - max degrees per tick we can spin, input speed (as a percentage -100 <= x <= 100), current position, and tick speed (how long to spin for)
    # Outputs: New position in degrees
    actualSpinSpeed = spinSpeed if -100 <= spinSpeed <= 100 else (sign(spinSpeed) * 100)
    newPosition = (actualSpinSpeed * maxDegreesPerTick * tick) + position
    return newPosition
    

Kp = 0.8
Ki = 0.0
Kd = 0.5
starti = 0

dt = 0.01 # time per PID tick
processValue = 0 # this would actually be a motor's position, and we would likely reset the position to zero whenever we start another movement
setPoint = 1200

t = 0 
maxT = 1 # timeout
settletime = 0.05
settlerange = 1.5
tickinterval = 0.01
maxRPM = 600

print("PID tests")
print(f"Gains: Kp = {Kp}, Ki = {Ki}, Kd = {Kd}, StartI = {starti}")
print(f"Setpoint: {setPoint} degrees")
print(f"Starting value: {processValue} degrees")
print(f"Tick interval: 1 tick per {tickinterval} seconds\n")

PID(processValue, setPoint, Kp, Ki, Kd, starti, settletime, settlerange, tickinterval, maxT, maxRPM)


# previous structure below

##prevError = processValue - setPoint # just creates a starting error to use
##starti = abs(prevError)
##accumulatedError = 0
##
##while t <= maxT:
##    err = setPoint - processValue
##    # If we're not further away from setPoint than where we started, allow accumulatedError to increase
##    if abs(err) < starti:
##        accumulatedError += err
##    # If processValue crosses over our setpoint, reset our accumulated error (which pretends we just started again from our old point)
##    # This prevents those huge compounding oscillations that swing crazily
##    if (err > 0 and prevError < 0) or (err < 0 and prevError > 0):
##        accumulatedError = 0
##    p = Kp * err
##    i = Ki * accumulatedError
##    d = Kd * (err - prevError)
##    # Pretend we can only move a value so fast with maxChangeSpeed
##    change = p + i + d if -maxChangeSpeed < p + i + d < maxChangeSpeed else sign(p + i + d) * maxChangeSpeed 
##    # (But we have perfect precision)
##    processValue += change 
##    prevError = err
##    t += dt
##    print(f"Process value: {processValue}")

