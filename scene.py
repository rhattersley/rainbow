from __future__ import division

import sphere, plane
from shaders import *

def _scenes(preview):
    global DiffuseShader, JitterShader, StratShader, ImportShader

    black = (0.0, 0.0, 0.0)
    darkGrey = (0.3, 0.3, 0.3)
    grey = (0.6, 0.6, 0.6)
    
    diffuseShader = DiffuseShader(dCol=grey)
    #simpleShader = SimpleShader(dCol=black, rCol=grey)
    simpleShader = SimpleShader(dCol=grey, rCol=black)
    jitterShader = JitterShader(dCol=(73/255, 150/255, 65/255))
    I = 100
    lightShader = LightShader(eCol=(I, I, I))

##    skyShader = LightProbeShader('rnl_probe.float', 900, 900)
##    skyShader = LightProbeShader('grace_probe.float', 1000, 1000)
    #uffiziSkyShader = LightProbeShader('uffizi_probe.float', 1500, 1500)

    skyShader = (SkyShader, (3.0,3.0,5.0), (1.0,0.0,0.5))
    uffiziSkyShader = (LightProbeShader, '/data/local/ithr/uffizi_probe.float', 1500, 1500)

    if preview:
        diffuseShader = simpleShader
        jitterShader = simpleShader

        DiffuseShader = SimpleShader
        JitterShader = SimpleShader
        StratShader = SimpleShader
        ImportShader = SimpleShader

    scenes = {
        'lights': {
            'sky': skyShader,
            'primitives': [
                    sphere.Sphere((0.0, 0.0, 0.0), 0.4, shader=jitterShader),
                    sphere.Sphere((0.6, 0.0, -0.3), 0.1, shader=lightShader),
            ]
        },
        'uffizi': {
            'sky': uffiziSkyShader,
            'primitives': [
                    #plane.Rect(orig=(0.0, -0.4, 0.0), n=(0,1,0), x=(1,0,0), w=0.6, h=0.6, shader=jitterShader),
                sphere.Sphere((-0.3,-0.1,0), 0.3, shader=jitterShader),
                sphere.Sphere((0.3,-0.2,0), 0.2, shader=SimpleShader(black, grey)),
                sphere.Sphere((0.10,-0.3,-0.15), 0.1, shader=LightShader(eCol=(4,4,4))),
            ]
        },
        'sphere': {
            'sky': skyShader,
            'primitives': [
                    sphere.Sphere((0.0, 0.0, 0.0), 0.4, shader=jitterShader),
            ]
        },
        'twoPlanes': {
            'sky': (SkyShader, (1.0,0.0,3.0), (3.0,0.0,0.0)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=SimpleShader(dCol=(0.9, 0.9, 0.9))),
                plane.Rect(orig=(0,0,0), n=(0,0,-0.5), x=(1,0,0), w=0.5, h=0.5, shader=SimpleShader(dCol=(0.9, 0.9, 0.9))),
            ]
        },
        'diffSpheres': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=DiffuseShader(dCol=(0.9, 0.9, 0.0))),
                sphere.Sphere((-0.2,0.1,0), 0.45, shader=DiffuseShader(dCol=(0.9,0.9,0.9))),
                sphere.Sphere((0.10,-0.22,-0.35), 0.1, shader=DiffuseShader(dCol=(0.9,0.9,0.9))),
            ]
        },
        'stratSpheres': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=StratShader(dCol=(0.9, 0.9, 0.0))),
                sphere.Sphere((-0.2,0.1,0), 0.45, shader=StratShader(dCol=(0.9,0.9,0.9))),
                sphere.Sphere((0.10,-0.22,-0.35), 0.1, shader=StratShader(dCol=(0.9,0.9,0.9))),
            ]
        },
        'jitterSpheres': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=JitterShader(dCol=(0.9, 0.9, 0.0))),
                sphere.Sphere((-0.2,0.1,0), 0.45, shader=JitterShader(dCol=(0.9,0.9,0.9))),
                sphere.Sphere((0.10,-0.22,-0.35), 0.1, shader=JitterShader(dCol=(0.9,0.9,0.9))),
            ]
        },
        'importSpheres': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=ImportShader(dCol=(0.9, 0.9, 0.0))),
                sphere.Sphere((-0.2,0.1,0), 0.45, shader=ImportShader(dCol=(0.9,0.9,0.9))),
                sphere.Sphere((0.10,-0.22,-0.35), 0.1, shader=ImportShader(dCol=(0.9,0.9,0.9))),
            ]
        },        
        'lightSpheres': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=JitterShader(dCol=(73/255, 150/255, 65/255))),
                sphere.Sphere((-0.2,0.1,0), 0.45, shader=JitterShader(dCol=(0.9,0.4,0.4))),
                sphere.Sphere((0.10,-0.201,-0.35), 0.1, shader=LightShader(eCol=(6.0,6.0,6.0))),
            ]
        },
        'lightSpheres2': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=JitterShader(dCol=(73/255, 150/255, 65/255))),
                sphere.Sphere((-0.2,0.1,0), 0.45, shader=JitterShader(dCol=(0.9,0.4,0.4))),
                sphere.Sphere((0.10,-0.201,-0.35), 0.1, shader=LightShader(eCol=(16.0,16.0,16.0))),
            ]
        },
        'box1': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.4,0), n=(0,1,0), shader=SimpleShader(dCol=(73/255, 150/255, 65/255))),
                plane.Rect(orig=(0,0.0,1.0), n=(0,0,-1), x=(-1,0,0), w=0.8, h=0.4, shader=SimpleShader(dCol=(150/255, 150/255, 150/255))),
                plane.Rect(orig=(-0.8,0.0,0.45), n=(1,0,0), x=(0,0,1), w=0.45, h=0.4, shader=SimpleShader(dCol=(150/255, 150/255, 150/255))),
                plane.Rect(orig=(0.8,0.0,0.5), n=(-1,0,0), x=(0,0,1), w=0.5, h=0.4, shader=SimpleShader(dCol=(150/255, 150/255, 150/255))),
                plane.Rect(orig=(0,0.4,0.5), n=(0,-1,0), x=(0,0,1), w=0.5, h=0.8, shader=SimpleShader(dCol=(150/255, 150/255, 150/255))),
                sphere.Sphere((-0.4,-0.2,0.5), 0.2, shader=SimpleShader(dCol=(0.9,0.4,0.4))),
                sphere.Sphere((0.0,-0.2,0.5), 0.2, shader=LightShader(eCol=(16.0,16.0,16.0))),
                sphere.Sphere((0.4,-0.2,0.5), 0.2, shader=SimpleShader(dCol=(0.9,0.4,0.4))),
            ]
        },
        'box2': {
            'sky': (SkyShader, (3.0,3.0,5.0), (3.0,3.0,3.5)),
            'primitives': [
                plane.Plane(orig=(0,-0.4,0), n=(0,1,0), shader=JitterShader(dCol=(73/255, 150/255, 65/255))),
                plane.Rect(orig=(0,0.0,1.0), n=(0,0,-1), x=(-1,0,0), w=0.8, h=0.4, shader=JitterShader(dCol=(150/255, 150/255, 150/255))),
                plane.Rect(orig=(-0.8,0.0,0.45), n=(1,0,0), x=(0,0,1), w=0.45, h=0.4, shader=JitterShader(dCol=(150/255, 150/255, 150/255))),
                plane.Rect(orig=(0.8,0.0,0.5), n=(-1,0,0), x=(0,0,1), w=0.5, h=0.4, shader=JitterShader(dCol=(150/255, 150/255, 150/255))),
                plane.Rect(orig=(0,0.4,0.5), n=(0,-1,0), x=(0,0,1), w=0.5, h=0.8, shader=JitterShader(dCol=(150/255, 150/255, 150/255))),
                sphere.Sphere((-0.4,-0.2,0.5), 0.2, shader=JitterShader(dCol=(0.9,0.4,0.4))),
                sphere.Sphere((0.0,-0.2,0.5), 0.2, shader=LightShader(eCol=(16.0,16.0,16.0))),
                sphere.Sphere((0.4,-0.2,0.5), 0.2, shader=JitterShader(dCol=(0.9,0.4,0.4))),
            ]
        },
        'threeSpheres': {
            'sky': (SkyShader, (1.0,0.0,3.0), (3.0,0.0,0.0)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(0,1,0), shader=SimpleShader(dCol=(0.9, 0.9, 0.9))),
                sphere.Sphere((-0.2,0.1,0), 0.45, shader=SimpleShader(dCol=(0.1,0.1,0.1), rCol=(0.7, 0.7, 0.5))),
                sphere.Sphere((0.2,-0.22,-0.47), 0.1, shader=SimpleShader(dCol=(0.8,0.0,0.0))),
                sphere.Sphere((-0.58,0.1,-0.2), 0.1, shader=SimpleShader(dCol=(0.0,0.0,1.0))),
            ]
        },
        'backup': {
            'sky': (SkyShader, (1.0,0.0,3.0), (3.0,0.0,0.0)),
            'primitives': [
                plane.Plane(orig=(0,-0.3,0), n=(-0.5,1,-0.2), shader=SimpleShader(dCol=(0.9, 0.9, 0.9))),
                sphere.Sphere((-0.2,0,0), 0.45, shader=SimpleShader(dCol=(0.1,0.1,0.1))),
                sphere.Sphere((0.0,-1000.3,0.0), 1000, shader=SimpleShader(dCol=(0.6,0.6,0.6), rCol=(0.2,0.2,0.2))),
                sphere.Sphere((0.0,-1000.3,0.0), 1000, shader=SimpleShader(dCol=(0.6,0.6,0.6))),
            ]
        },
    }
    return scenes


def scene_names():
    return _scenes(False).keys()


def getScene(id, preview):
    scene = _scenes(preview)[id]
    if preview:
        scene['sky'] = SkyShader((3.0,3.0,5.0), (3.0,3.0,3.5))
    else:
        scene['sky'] = scene['sky'][0](*scene['sky'][1:])
    return scene
