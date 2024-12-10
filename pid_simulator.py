class PID():
    def __init__(self, pv, sp, kp, ki, kd, exitRange, exitTime, timeout, starti=0):
        self.pv = pv
        self.sp = sp
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.exitRange = exitRange
        self.exitTime = exitTime
        self.timeout = timeout
        self.starti = starti
        
        self.acc_i = 0
        self.err = sp-pv
        self.timeSettled = 0
        self.prevErr = 0
        self.timeSpent = 0
        # "Physical" constants
        self.speed = 0
        self.maxSpeed = 50
        self.maxAccel = 150
        self.timestep = 0.005

        self.idealTime = self.calculate_travel_time()
        
    def calculate_travel_time(self):
        abs_err = abs(self.sp - self.pv)  # Absolute error
        if abs_err < self.exitRange:
            # Already within the exit range, just wait for exitTime
            return self.exitTime

        t_acc = self.maxSpeed / self.maxAccel  # Time to reach max speed
        d_acc = 0.5 * self.maxAccel * t_acc ** 2  # Distance covered during acceleration
        D_settle_start = abs_err - self.exitRange

        if d_acc >= D_settle_start:
            # If we can reach the exit range just by accelerating
            t_reach = pow((2 * D_settle_start / self.maxAccel), 0.5)
        else:
            # We reach max speed and then need to travel some distance at max speed
            d_const = D_settle_start - d_acc
            t_const = d_const / self.maxSpeed
            t_reach = t_acc + t_const

        T = t_reach + self.exitTime
        return T
    
    def compute(self):
        self.err = self.sp-self.pv
        
        if abs(self.err) < self.starti:
            self.acc_i += self.err*self.timestep
        if (self.err>0 and self.prevErr<0) or (self.err<0 and self.prevErr>0):
            self.acc_i = 0
            
        p = self.kp * self.err
        i = self.ki * self.acc_i
        d = self.kd*(self.err - self.prevErr)/self.timestep
        
        self.prevErr = self.err
        
        if abs(self.err) < self.exitRange:
            self.timeSettled += self.timestep
        else:
            self.timeSettled = 0
        self.timeSpent += self.timestep
        
        return p+i+d

    def simulate(self, power): # pretend we're actually moving something
        self.speed += self.clamp(power, self.maxAccel*self.timestep) # add on to the speed
        self.speed = self.clamp(self.speed, self.maxSpeed) # but we can't go faster than the max speed
        self.pv += self.speed * self.timestep # position changed by speed * time
        return self.pv

    def sgn(self, x):
        return 1 if x > 0 else -1 if x < 0 else 0
    
    def clamp(self, x, bound):
        if abs(x)>bound:
            return self.sgn(x)*bound
        return x

    def isSettled(self):
        if self.timeSpent > self.timeout and self.timeout != 0:
            print("OUT OF TIME")
            return True
        if self.timeSettled > self.exitTime:
            return True
        return False
        
pv, sp = 0, 100
pid = PID(
    pv,     # starting point
    sp,     # ending point
    4.2,    # kP
    0.5,    # kI
    0.7,    # kD
    0.3,    # exit range
    0.5,    # exit time
    10,     # timeout
    10      # integral range
)

# best so far: 3.6, 0.2, 0.6, si = 8

i = 0
while not(pid.isSettled()):
    i += 1
    val = pid.compute()
    pid.simulate(val)
    # uncomment the below line to see each timestep
    # print("position:", round(pid.pv, 5), "speed:", round(pid.speed, 6), "at time:", round(pid.timestep*i, 5))
    if i > 10000:
        print("timed out after", i*pid.timestep, "seconds")
        break
else:
    print("final pos:", pid.pv, "desired pos:", pid.sp, "final error:", pid.err)
    print("we settled after", i, "iters at", pid.timestep*1000, "milliseconds per step, which is", round(i*pid.timestep, 5), "seconds")
    print("absolutely perfect time would have been", round(pid.idealTime, 5), "seconds (no deceleration)")

