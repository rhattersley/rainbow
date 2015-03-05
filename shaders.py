from math import acos, sqrt, ceil, pi
from random import uniform
import struct

from ray import *
from tracer import trace, checkIntersection

lD = normalise(-0.4,0.5,-0.4)
#lD = normalise(-1,1,0.3)
lCol = (10.0,9.0,3.0)
alCol = (1.0,2.0,3.0)

class SimpleShader2:
    def __init__(self, dCol, rCol=None):
        pass

class SimpleShader:
    def __init__(self, dCol, rCol=None):
        self.dCol = dCol
        self.rCol = rCol

        # NB. For a two-tone grid shader
##        if (floor(dx*10)+floor(dy*10))%2:
##            self.dCol=self._dCol
##        else:
##            self.dCol=(0,0,0)

    def shade(self, i, ray, contrib):
        if contrib < 0.05: return (0.0,0.0,0.0)
        
        # Ambient
        aCol=[va*vd for va,vd in zip(alCol, self.dCol)]

        # Diffuse
        lRay = Ray([pv+0.000001*dv for pv,dv in zip(i.p, lD)], lD)
        if checkIntersection(lRay):
            dCol = [0,0,0]
        else:
            dp = max(dot(i.n, lD), 0)
            dCol=[vl*vd*dp for vl,vd in zip(lCol, self.dCol)]

        # Specular
        rCol = [0,0,0]
        if self.rCol is not None:
            rRay = ray.getReflection(i.p, i.n)
            rtCol = trace(rRay, contrib * max(self.rCol))
            rCol = [vt*vr for vt,vr in zip(rtCol, self.rCol)]

        return [sum(v) for v in zip(aCol,dCol,rCol)]
    
class DiffuseShader:
    def __init__(self, dCol):
        self.dCol = dCol

    def shade(self, hit, ray, contrib):
        if contrib < 0.05: return (0.0,0.0,0.0)
        iCol = [0,0,0]
        n = 16
        r=1.0/n
        contrib = contrib * max(self.dCol) * r
        for i in range(n):
            ray = getRayFromHemisphere(hit.p, hit.n)
            rCol = trace(ray, contrib)
            dp = max(dot(hit.n, ray.d), 0)
            iCol=[vi+vr*dp for vi,vr in zip(iCol, rCol)]

        return [vi*vd*r for vi,vd in zip(iCol, self.dCol)]
    
class StratShader:
    def __init__(self, dCol):
        self.dCol = dCol

    def shade(self, hit, ray, contrib):
        if contrib < 0.05: return (0.0,0.0,0.0)
        iCol = [0,0,0]
        n = 3
        df=1.0/n
        cf=1.0/(n*n)
        contrib = contrib * max(self.dCol) * cf
        for u in range(n):
            u=(u+0.5)*df
            for v in range(n):
                v=(v+0.5)*df
                ray = getRayFromHemisphereUniform(hit.p, hit.n, u, v)
                rCol = trace(ray, contrib)
                dp = max(dot(hit.n, ray.d), 0)
                iCol=[vi+vr*dp for vi,vr in zip(iCol, rCol)]

        return [vi*vd*cf for vi,vd in zip(iCol, self.dCol)]

class JitterShader:
    def __init__(self, dCol):
        self.dCol = dCol

    def shade(self, hit, ray, contrib):
        if contrib < 0.003: return (0.0,0.0,0.0)
        iCol = [0,0,0]
        n = int(ceil(sqrt(256*sqrt(contrib))))
        df=1.0/n
        cf=1.0/(n*n)
        contrib = contrib * max(self.dCol) * cf
        for u in range(n):
            u=(u+uniform(0.0,1.0))*df
            for v in range(n):
                v=(v+uniform(0.0,1.0))*df
                ray = getRayFromHemisphereUniform(hit.p, hit.n, u, v)
                rCol = trace(ray, contrib)
                dp = max(dot(hit.n, ray.d), 0)
                iCol=[vi+vr*dp for vi,vr in zip(iCol, rCol)]

        return [vi*vd*cf for vi,vd in zip(iCol, self.dCol)]

# XXX Flawed!
class ImportShader:
    def __init__(self, dCol):
        self.dCol = dCol

    def shade(self, hit, ray, contrib):
        if contrib < 0.05: return (0.0,0.0,0.0)
        iCol = [0,0,0]
        n = 4
        df=1.0/n
        cf=1.0/(n*n)
        contrib = contrib * max(self.dCol) * cf
        for u in range(n):
            u=(u+uniform(0.25,0.75))*df
            for v in range(n):
                v=(v+uniform(0.25,0.75))*df
                i, ray = getRayFromHemisphereCos(hit.p, hit.n, u, v)
                rCol = trace(ray, contrib)
                dp = max(dot(hit.n, ray.d), 0)
                iCol=[vi+vr*dp/i for vi,vr in zip(iCol, rCol)]

        return [vi*vd*cf for vi,vd in zip(iCol, self.dCol)]

class LightShader:
    def __init__(self, eCol):
        self.eCol = eCol

    def shade(self, hit, ray, contrib):
        cf = 0.5-0.5*dot(hit.n, ray.d)
        return [ve*cf for ve in self.eCol]

class Sky(object):
    def getColour(self, d):
        raise NotImplementedError

class SkyShader(Sky):
    def __init__(self, zCol, hCol):
        self.zCol = zCol
        self.hCol = hCol
        
    def getColour(self, d):
        zF = abs(dot(d, (0,1,0)))
        hF = 1-zF
        return [zF*vz+hF*vh for vz,vh in zip(self.zCol,self.hCol)]

class LightProbeShader2(Sky):
    s = 1.0 / pi
    
    def __init__(self, path, w, h):
        f = open(path, 'rb')
        image = []
        pixelFormat = '<fff'
        pixelSize = struct.calcsize(pixelFormat)
        for y in range(h):
            row = []
            for x in range(w):
                data = f.read(pixelSize)
                pixel = struct.unpack(pixelFormat, data)
                row.append(pixel)
            image.append(row)
        self.image = image

        self.w = w / 2
        self.h = h / 2

    def getColour(self, d):
        r = self.s * acos(d[2]) / sqrt(d[0] * d[0] + d[1] * d[1])
        u = ((d[0] * r) + 1) * self.w
        v = ((d[1] * r) + 1) * self.h
        return self.image[int(v)][int(u)]

import numpy
class LightProbeShader(Sky):
    s = 1.0 / pi
    
    def __init__(self, path, w, h):
        self.image = numpy.fromfile(path, dtype='<f')
        self.image.shape = (h, w, 3)

        self.w = w / 2
        self.h = h / 2

    def getColour(self, d):
        r = self.s * acos(d[2]) / sqrt(d[0] * d[0] + d[1] * d[1])
        u = ((d[0] * r) + 1) * self.w
        v = ((d[1] * r) + 1) * self.h
        return self.image[int(v), int(u)]
