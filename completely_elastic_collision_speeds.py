def CEC(m1, m2, v1, v2):
    # return in format v1', v2'
    v2prime = ((2*m1*v1 + v2 * (m2-m1))/(m1+m2))
    return ((m1*v1 + m2*v2 - m2*v2prime)/m1), v2prime

def CEC2(m1, v1, m2, v2=0):
    v1prime = (2*m2*v2 + v1 * (m1-m2))/(m1+m2)
    v2prime = (m1*v1 + m2*v2 - m1*v1prime)/m2
    return v1prime, v2prime

def c(m1, v1, m2, v2=0):
    print("version 1", CEC(m1,m2,v1,v2))
    print("version 2", CEC2(m1,v1,m2,v2))
