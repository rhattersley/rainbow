from ray import dot, normalise, cross, neg
import intersection
from math import floor

class Plane:
    def __init__(self, orig, n, shader):
        self.orig = orig
        self.n = normalise(*n)
        self.shader = shader

        self.d = -dot(self.orig, self.n)

    def getIntersection(self, ray):
        temp = dot(ray.d, self.n)
        if abs(temp) < 1e-6: return None

        t = -(dot(ray.o, self.n)+self.d)/temp
        if t < 0: return None

        p = [0,0,0]
        for i in range(3):
            p[i] = ray.o[i]+t*ray.d[i]

        return (p, t)

    def intersect(self, ray):
        temp = self.getIntersection(ray)
        if temp is None: return None
        return intersection.Intersection(self, temp[0], temp[1], self.n)
        
class Rect(Plane):
    def __init__(self, orig, n, x, w, h, shader):
        Plane.__init__(self, orig, n, shader)

        self.x = normalise(*x)
        self.y = neg(cross(self.n, self.x))
        self.w = w
        self.h = h

    def intersect(self, ray):
        temp = self.getIntersection(ray)
        if temp is None: return None
        p, t = temp

        dp = [0,0,0]
        for i in range(3):
            dp[i]=p[i]-self.orig[i]
        u=dot(dp, self.x)
        if abs(u) > self.w: return None
        v=dot(dp, self.y)
        if abs(v) > self.h: return None
        
        return intersection.Intersection(self, temp[0], temp[1], self.n)
