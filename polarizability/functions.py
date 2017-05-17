import math

def dprmtr_def(h,k,l,a,b,c,alfa,beta,gamma):
    up_1 = (math.pow(h/a*math.sin(alfa),2)) + (math.pow(k/b*math.sin(beta),2)) + (math.pow(l/c*math.sin(gamma),2))
    up_2 = math.cos(alfa)*2*k*l/b/c + math.cos(beta)*2*h*l/a/c + math.cos(gamma)*2*h*k/a/b
    up = up_1 + up_2
    down = 1 - math.pow(math.cos(alfa),2) - math.pow(math.cos(beta),2) - math.pow(math.cos(gamma),2) + 2 * math.cos(alfa) * math.cos(beta) * math.cos(gamma)
    return math.sqrt(down/up)
