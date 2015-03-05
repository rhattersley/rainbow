import numpy as np
import screen
from ray import dot, normalise, Ray
from random import uniform

skyShader = None
primitives = []

def getImage(scene, resX, resY, ss, x1, y1, x2, y2):
    global skyShader, primitives
    skyShader = scene['sky']
    primitives = scene['primitives']

    dss=1.0/ss
    css=1.0/(ss*ss)

    image = np.zeros((y2 - y1, x2 - x1, 3), dtype=np.float32)

    if ss > 1:
        for y in range(y2 - y1):
            row = []
            for x in range(x2 - x1):
                c = [0,0,0]
                for sx in range(ss):
                    xss = x1+x+(sx+uniform(-0.5,0.5))*dss
                    for sy in range(ss):
                        yss = y1+y+(sy+uniform(-0.5,0.5))*dss
                        ray = screen.getRay(xss, yss, resX, resY)
                        ct = trace(ray, css)
                        for i in range(3):
                            c[i] += ct[i]
                c = [cv*css for cv in c]
                image[y, x, :] = c
    else:
        for y in range(y2 - y1):
            row = []
            for x in range(x2 - x1):
                ray = screen.getRay(x+x1, y+y1, resX, resY)
                c = trace(ray, 1.0)
                image[y, x, :] = c

    return image

def trace(ray, contrib):
    i = getIntersection(ray)
    if i is None:
        return skyShader.getColour(ray.d)
    else:
        return i.obj.shader.shade(i, ray, contrib)

def getIntersection(ray):
    nearest = None
    nearestObj = None
    for obj in primitives:
        i = obj.intersect(ray)
        if i is None: continue
        if nearest is None or i.t < nearest.t:
            nearest=i
    return nearest

def checkIntersection(ray):
    for obj in primitives:
        i = obj.intersect(ray)
        if i is not None: return True
    return False
