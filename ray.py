from math import sqrt, pi, sin, cos
from random import uniform

class Ray:
    def __init__(self, o, d):
        self.o = o
        self.d = d

    def getReflection(self, p, n):
        # R = V - ( 2 * V [dot] N ) N
        f = 2.0*dot(self.d, n)
        rd = [self.d[i]-f*n[i] for i in range(3)]
        p = [p[i]+0.000001*rd[i] for i in range(3)]
        return Ray(p, rd)

    def __str__(self):
        v = tuple([float(x) for x in list(self.o)+list(self.d)])
        return 'Ray: (%f,%f,%f) + t(%f,%f,%f)' % v
        
def dot(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]

def normalise(x,y,z):
    l=sqrt(x*x+y*y+z*z)
    return x/l, y/l, z/l

def cross(v1, v2):
    return (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0])

def neg(v):
    return (-v[0], -v[1], -v[2])

def getPointFromS2():
    while True:
        x=uniform(-1,1)
        y=uniform(-1,1)
        z=uniform(-1,1)
        r2=x*x+y*y+z*z
        if 0.001<r2 and r2<1.0:
            return normalise(x,y,z)

def getRayFromHemisphere(p,n):
    x,y,z = getPointFromS2()
    if dot((x,y,z), n) < 0:
        x,y,z=-x,-y,-z
    d=(x,y,z)
    return Ray([p[i]+0.000001*d[i] for i in range(3)], d)

pi2 = 2*pi

def getFrameFromNormal2(n):
    n1=list(n)
    i=2
    if abs(n[0]) > 0.7:
        i=0
    elif abs(n[1]) > 0.7:
        i=1
    n1[i]=2*n1[i]
    n1[(i+1)%3]=1+n1[(i+1)%3]
    n1=cross(n,n1)
    n1=normalise(*n1)
    n2=cross(n,n1)
    return n1,n2

def getFrameFromNormal3(n):
    if abs(n[1]) < 1.0:
        n1=[n[0],0.0,n[2]]
        n1=cross(n,n1)
        try:
            n1=normalise(*n1)
        except:
            print n, n1
    else:
        n1=[1.0,0.0,0.0]
    n2=cross(n,n1)
    return n1,n2

def getFrameFromNormal(n):
    a = abs(n[1])
    if a > 0.95:
        n1=[1.0,0.0,0.0]
    elif a > 0.1:
        n1=[n[0],0.0,n[2]]
    else:
        n1=[n[0],1.0,n[2]]
    n1=cross(n,n1)
    n1=normalise(*n1)
    
    n2=cross(n,n1)
    return n1,n2

def getRayFromHemisphereUniform(p,n,u,v):
    # Assuming n is (0,0,1)
    u=1-u # Kinda irrelevant
    t1 = sqrt(1-u*u)
    t2 = pi2*v
    x = t1*cos(t2)
    y = t1*sin(t2)
    z = u

    n1,n2 = getFrameFromNormal(n)
    d=(x*n1[0]+y*n2[0]+z*n[0],x*n1[1]+y*n2[1]+z*n[1],x*n1[2]+y*n2[2]+z*n[2])
    return Ray([p[i]+0.000001*n[i] for i in range(3)], d)

def getRayFromHemisphereCos(p,n,u,v):
    # Assuming n is (0,0,1)
    u=1-u # Kinda irrelevant
    t1 = sqrt(1-u)
    t2 = pi2*v
    x = t1*cos(t2)
    y = t1*sin(t2)
    z = u

    n1,n2 = getFrameFromNormal(n)
    d=(x*n1[0]+y*n2[0]+z*n[0],x*n1[1]+y*n2[1]+z*n[1],x*n1[2]+y*n2[2]+z*n[2])
    # XXX Importance scaling??
    return (pi*cos(u)/2, Ray([p[i]+0.000001*d[i] for i in range(3)], d))

if __name__ == '__main__':
    print getFrameFromNormal(normalise(1.0,0.0,0.0))
    print getFrameFromNormal(normalise(1.0,1.0,0.0))
    print getFrameFromNormal(normalise(1.0,1.0,1.0))

