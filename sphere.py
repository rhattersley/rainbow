import math
import intersection
from ray import Ray, dot, normalise, getPointFromS2

XYZ = (0,1,2)

class Sphere:
    def __init__(self, orig, radius, shader):
        self.orig = orig
        self.radius = radius
        self.shader = shader

    def intersect(self, ray):
        r = self.radius

        rayO = [0,0,0]
        for i in range(3):
            rayO[i] = ray.o[i] - self.orig[i]
    
        # Compute A, B and C coefficients
        # a = dot(ray.d, ray.d)
        # print 'a = ',a
        a = 1.0
        b = 2 * dot(ray.d, rayO)
        c = dot(rayO, rayO) - (r * r)

        # Find discriminant
        disc = b * b - 4 * a * c

        # if discriminant is negative there are no real roots, so return 
        # false as ray misses sphere
        if (disc < 0):
            return None;

        # compute q as described above
        distSqrt = math.sqrt(disc)
        if (b < 0):
            q = (-b - distSqrt)/2.0
        else:
            q = (-b + distSqrt)/2.0

        if abs(q) < 1e-6: return None

        # compute t0 and t1
        t0 = q / a;
        t1 = c / q;

        # make sure t0 is smaller than t1
        if (t0 > t1):
            # if t0 is bigger than t1 swap them around
            t0,t1=t1,t0

        # if t1 is less than zero, the object is in the ray's negative direction
        # and consequently the ray misses the sphere
        if (t1 < 0):
            return None

        # if t0 is less than zero, the intersection point is at t1
        if (t0 < 0):
            t = t1;
        # else the intersection point is at t0
        else:
            t = t0;

        p = [0,0,0]
        n = [0,0,0]
        for i in range(3):
            p[i] = ray.o[i]+t*ray.d[i]
            n[i] = p[i]-self.orig[i]
        n = normalise(*n)
            
        return intersection.Intersection(self, p, t, n)
    
    def getSurfaceRay(self):
        n=getPointFromS2()
        o=self.orig
        r=self.radius*1.0001
        return Ray([o[i]+n[i]*r for i in XYZ], n)
    
